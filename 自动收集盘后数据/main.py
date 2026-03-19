import logging
import os
import shutil
import sys
import time
import requests
import traceback
from multiprocessing import Process, Event
from pynput import keyboard as pynput_keyboard

from pywinauto import Application
from pywinauto.timings import wait_until_passes
from pywinauto import keyboard, mouse

from convertlc import batch_convert_lc5, tidy_lc5_result
from copyvalue import copy_value

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    stream=sys.stdout  # 明确输出到 stdout
)


def click_control(control, timeout=10, use_mouse=True):
    """
    点击指定的 pywinauto 控件

    :param control: pywinauto 控件对象（如 dlg.child_window(...)）
    :param timeout: 等待控件启用的超时时间（秒）
    :param use_mouse: True 使用真实鼠标点击（推荐），False 使用 .click() 消息触发
    """
    try:
        # 等待控件存在并启用
        control.wait("exists enabled", timeout=timeout)

        if use_mouse:
            # 获取控件屏幕坐标
            rect = control.rectangle()
            x = (rect.left + rect.right) // 2
            y = (rect.top + rect.bottom) // 2

            # 可选：短暂延迟确保界面稳定
            time.sleep(0.1)

            # 模拟真实鼠标点击
            mouse.click(coords=(x, y))
        else:
            # 使用 pywinauto 内置 click（发送 WM_CLICK）
            control.click()

    except TimeoutError:
        raise RuntimeError(f"控件未在 {timeout} 秒内变为可用: {control}")
    except Exception as e:
        raise RuntimeError(f"点击控件时出错: {e}")


def get_listview_items(listview):
    """
    尝试获取 SysListView32 的所有可见项目内容。
    适用于 backend='win32'。
    """
    try:
        listview.set_focus()
    except Exception:
        pass  # 忽略聚焦失败

    item_count = listview.item_count()

    if item_count == 0:
        print("[WARN] ListView 为空或无法读取内容")
        return []

    all_rows = []

    # 尝试读取第一项，判断是否支持分列
    try:
        first_item = listview.get_item(0)
        # 方法1：尝试获取子项（多列）
        col0_text = first_item.get_sub_item(0).text()
        # 如果成功，说明支持多列
        supports_subitems = True
        # 动态探测列数（最多试10列）
        col_count = 0
        for j in range(10):
            try:
                first_item.get_sub_item(j)
                col_count = j + 1
            except Exception:
                break
    except Exception as e:
        supports_subitems = False

    # 逐行读取
    for i in range(item_count):
        try:
            if supports_subitems:
                row = []
                for j in range(col_count):
                    try:
                        text = listview.get_item(i).get_sub_item(j).text()
                        row.append(text)
                    except Exception:
                        row.append("")
                all_rows.append(row)
            else:
                # 单列或整行文本
                text = listview.get_item(i).text()
                all_rows.append([text])
        except Exception as e:
            print(f"[ERROR] 读取第 {i} 行失败: {e}")
            all_rows.append([""])

    return all_rows


def base_ready(app, dlg, start_time, end_time):
    dlg.set_focus()
    dlg.child_window(title="清空品种", class_name="Button").click()

    try:
        confirm_dlg = app.window(title="TdxW")
        confirm_dlg.wait("visible", timeout=0.5)
        confirm_dlg.set_focus()

        confirm_dlg.child_window(title="是(&Y)", class_name="Button").click()

    except Exception as e:
        logging.warning("未检测到确认对话框")

    if not dlg.child_window(title="5分钟线数据", class_name="Button").is_checked():
        dlg.child_window(title="5分钟线数据", class_name="Button").click()
        logging.info("选中5分钟线")
    else:
        logging.info("5分钟线已经选中")

    date_pickers = dlg.children(class_name="SysDateTimePick32")

    start_time = list(map(int, start_time.split("-")))
    end_time = list(map(int, end_time.split("-")))

    date_pickers[0].set_time(year=start_time[0], month=start_time[1], day=start_time[2], day_of_week=0)
    date_pickers[1].set_time(year=end_time[0], month=end_time[1], day=end_time[2], day_of_week=0)


def download_data(start_time: str, end_time: str, stock_ids: list) -> bool:
    app = Application(backend="win32").connect(title="盘后数据下载")
    dlg = app.window(title="盘后数据下载")

    tab = dlg.child_window(class_name="SysTabControl32")
    tab.select(1)  # 切换到沪深分钟线

    add_button = dlg.child_window(title="添加品种", class_name="Button")

    base_ready(app, dlg, start_time, end_time)

    temp_stock_ids = [id_ for id_ in stock_ids if len(id_) == 6]
    temp_index = 0

    while temp_index < len(temp_stock_ids):

        stock_id = temp_stock_ids[temp_index]

        # 关闭之前的窗口
        try:
            choose_dlg = app.window(title="选择品种(沪深京品种)")
            choose_dlg.wait("exists", timeout=0.1)
            choose_dlg.close()
        except Exception as e:
            pass

        try:
            add_button.click()

            choose_dlg = app.window(title="选择品种(沪深京品种)")
            choose_dlg.wait("ready", timeout=0.5)
            choose_dlg.set_focus()

            logging.info(f"Type: {stock_id}")
            choose_dlg.type_keys(stock_id)
            keyboard.send_keys("{ENTER}")
            time.sleep(0.1)

            lst_dlg = dlg.child_window(title="CFQS", class_name="SysListView32")

            for v in get_listview_items(lst_dlg):
                if v[0] == stock_id:
                    temp_index += 1
                    continue

        except Exception as e:
            continue

    tab.select(4)  # 切换到沪深分钟线

    # 判断是否有弹窗
    time.sleep(0.5)
    try:
        choose_dlg = app.window(title="扩展市场行情")
        choose_dlg.wait_not("exists", timeout=0.5)
    except Exception as e:
        pass

    add_button = dlg.child_window(title="添加品种", class_name="Button")

    base_ready(app, dlg, start_time, end_time)

    temp_stock_ids = [id_ for id_ in stock_ids if len(id_) == 5]
    temp_index = 0

    while temp_index < len(temp_stock_ids):

        stock_id = temp_stock_ids[temp_index]

        # 关闭之前的窗口
        try:
            choose_dlg = app.window(title="选择品种(扩展市场行情品种)")
            choose_dlg.wait("exists", timeout=0.1)
            choose_dlg.close()
        except Exception as e:
            pass

        try:
            add_button.click()

            choose_dlg = app.window(title="选择品种(扩展市场行情品种)")
            choose_dlg.wait("ready", timeout=0.5)

            choose_dlg.set_focus()

            choose_dlg.type_keys(stock_id)

            logging.info(f"Type: {stock_id}")
            keyboard.send_keys("{ENTER}")
            time.sleep(0.1)

            lst_dlg = dlg.child_window(title="CFQS", class_name="SysListView32")

            for v in get_listview_items(lst_dlg):
                if v[0] == stock_id:
                    temp_index += 1
                    continue

        except Exception as e:
            continue

    dlg.set_focus()
    click_control(dlg.child_window(title="开始下载", class_name="Button"))
    time.sleep(3)
    while True:
        try:
            dlg.child_window(title="下载完毕.", class_name="Static").wait("exists", timeout=30)
            return True
        except Exception as e:
            dlg.set_focus()
            try:
                click_control(dlg.child_window(title="开始下载", class_name="Button"))
            except Exception as e:
                pass


def clear_download_data(path=r'D:\new_tdx\vipdoc'):
    for filename in os.listdir(path):
        if os.path.isdir(os.path.join(path, filename)):
            clear_download_data(os.path.join(path, filename))
        elif filename.endswith(".lc5"):
            os.remove(os.path.join(path, filename))
            logging.info("Delete: " + os.path.join(path, filename))

    shutil.rmtree('./lc5')
    shutil.rmtree('./parsed_data')

    os.mkdir('./lc5')
    os.mkdir('./parsed_data')


def copy_download_data(path=r'D:\new_tdx\vipdoc'):
    for filename in os.listdir(path):
        if os.path.isdir(os.path.join(path, filename)):
            copy_download_data(os.path.join(path, filename))
        elif filename.endswith(".lc5"):
            shutil.copy(os.path.join(path, filename), os.path.join(os.path.abspath('./lc5'), filename))
            logging.info(f"Copy {os.path.join(path, filename)} => {os.path.join(os.path.abspath('./lc5'), filename)}")


def get_stock_percent(fund_code, start_time):
    response = requests.get(
        f"https://danjuanfunds.com/djapi/fundx/base/fund/record/asset/percent?fund_code={fund_code}&report_date={start_time}",
        headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0',
            'sec-ch-ua': '"Chromium";v="142", "Microsoft Edge";v="142", "Not_A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
    )
    response.raise_for_status()

    data = response.json()['data']['stock_list']

    # 使用字典按股票代码去重，保留占比最高的记录
    stock_dict = {}
    for item in data:
        code = item["code"]
        percent = item["percent"]
        # 如果该代码未出现过，或当前占比更高，则更新
        if code not in stock_dict or percent > stock_dict[code]["percent"]:
            stock_dict[code] = {
                "code": code,
                "name": item["name"],
                "percent": percent
            }

    # 转为列表
    stocks = [
        [item["code"], item["name"], item["percent"]]
        for item in stock_dict.values()
    ]

    # 按股票占比降序排序
    stocks.sort(key=lambda x: x[2], reverse=True)

    # 返回前10只
    return stocks[:10]


def run_download_in_process(fund_name, fund_code, time_list):
    """
    在子进程中运行下载任务。
    注意：stop_event 在子进程中无法被父进程直接设置，仅作占位。
    实际终止靠 os.kill。
    """
    try:

        for start_time, end_time in time_list:

            logging.info("准备清理之前的下载文件......")

            clear_download_data()

            logging.info("准备访问基金数据......")

            logging.info(f"正在获取 {fund_name}({fund_code}) 的 {start_time} 到 {end_time} 的数据")

            percent = get_stock_percent(fund_code, start_time)
            logging.info("持仓占比：" + str(percent))

            if len(percent) != 10:
                logging.error("程序提前终止！因为股票数量错误！")
                return False

            while True:

                stock_ids = [code for code, _, _ in percent]

                result = download_data(start_time, end_time, stock_ids)

                if result:
                    break

                logging.error("任务失败，重试下载任务。")

            logging.info("下载完毕，准备处理文件......")

            copy_download_data()

            target_path = r'./parsed_data'
            batch_convert_lc5(target_path=target_path)

            tidy_lc5_result(target_path, percent, f'./{fund_name} {start_time} 至 {end_time}')

        logging.info("任务完成。")
    except Exception as e:
        logging.error("❌ 下载任务异常:", e)
        traceback.print_exc()


def on_f12_press(key):
    """监听 F12 按下"""
    if key == pynput_keyboard.Key.f12:
        print("\n🛑 检测到 F12，正在终止下载任务...")
        return False  # 停止监听器
    return True


def main():
    config_string = """南方半导体产业股票发起A 020553
海富通中小盘混合 519026
博时厚泽匠选一年持有期混合A 018217
中欧半导体产业股票发起C 019764"""
    # config_string = ("招商优势企业混合 217021\n"
    #                  "天弘恒生科技指数C 012349\n"
    #                  "嘉实科技创新 007343\n"
    #                  "景顺长城中证港股通科技ETF 513980")

    valid_string = ""

    for line in config_string.split('\n'):
        name, code = line.split(' ')

        # 启动下载子进程
        proc = Process(target=run_download_in_process, args=(name, code, (
            ("2025-06-30", "2025-10-22"),
            ("2025-03-31", "2025-06-30"),
            ("2024-12-31", "2025-03-31"),
            ("2024-09-30", "2024-12-31"),
            ("2024-06-30", "2024-09-30"),
            ("2024-03-31", "2024-06-30"),
            ("2023-12-31", "2024-03-30")
        )))
        proc.start()

        print("🚀 下载任务已启动（按 F12 强制终止）")

        # 启动 F12 监听器
        with pynput_keyboard.Listener(on_press=on_f12_press) as listener:

            try:
                while proc.is_alive():
                    if not listener.running:
                        break
                    time.sleep(0.1)
            finally:
                listener.stop()
                listener.join()

        # 终止子进程（强制）
        if proc.is_alive():
            print("💀 强制终止下载进程...")
            proc.terminate()  # 发送 SIGTERM
            proc.join(timeout=3)  # 等待 3 秒
            if proc.is_alive():
                proc.kill()  # SIGKILL（Windows 上等效）
            print("✅ 进程已终止")

    for filename in os.listdir('.'):
        if filename.startswith(name):
            valid_string += name + ' ' + code + '\n'
            logging.info(f"{name} 获取有效。")
            break

    valid_string = valid_string.strip()
    if valid_string:
        copy_value(valid_string)

    logging.info("全部程序执行完毕")


if __name__ == '__main__':
    main()
