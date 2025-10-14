import asyncio
import json
import random

from playwright.async_api import async_playwright, expect

GET_FORM_BUTTON_CODE = """(data_form) => {
    // 通用版本 - 自动适配 Vue 2 和 Vue 3，查找包含 continueAnswer 方法的组件
    function findComponentWithContinueAnswer() {
      // 尝试找到根元素
      const possibleRoots = [
        document.getElementById('app'),
        document.getElementById('root'),
        document.querySelector('[data-app]'),
        ...document.querySelectorAll('div[id]')
      ].filter(Boolean);
      
      for (let rootElement of possibleRoots) {
        // 检查是否为 Vue 2
        if (rootElement.__vue__) {
          console.log('检测到 Vue 2 应用');
          return findInVue2Tree(rootElement.__vue__);
        }
        
        // 检查是否为 Vue 3
        if (rootElement.__vueParentComponent) {
          console.log('检测到 Vue 3 应用');
          return findInVue3Tree(rootElement.__vueParentComponent);
        }
      }
      
      console.warn('未找到 Vue 应用实例');
      return null;
    }
    
    // Vue 2 查找函数
    function findInVue2Tree(instance) {
      if (typeof instance.continueAnswer === 'function') {
        return instance;
      }
      
      if (instance.$children && instance.$children.length > 0) {
        for (let child of instance.$children) {
          const found = findInVue2Tree(child);
          if (found) return found;
        }
      }
      
      return null;
    }
    
    // Vue 3 查找函数
    function findInVue3Tree(component) {
      if (component.proxy && typeof component.proxy.continueAnswer === 'function') {
        return component.proxy;
      }
      
      // 检查子组件
      const checkChildren = (children) => {
        if (!children) return null;
        
        if (Array.isArray(children)) {
          for (let child of children) {
            if (child && child.component) {
              const found = findInVue3Tree(child.component);
              if (found) return found;
            }
          }
        } else if (children.component) {
          return findInVue3Tree(children.component);
        }
        
        return null;
      };
      
      // 检查 subTree
      if (component.subTree) {
        const found = checkChildren(component.subTree);
        if (found) return found;
      }
      
      // 检查其他可能的子组件引用
      if (component.vnode && component.vnode.children) {
        const found = checkChildren(component.vnode.children);
        if (found) return found;
      }
      
      return null;
    }
    
    targetComponent = findComponentWithContinueAnswer();
    targetComponent.setTotalAnswer(data_form);
    targetComponent.$emit("reRenderPage", !0)
}
"""

async def wjx(url, text_to_fill):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        page = await context.new_page()

        await page.goto(url)

        while True:
            try:
                await expect(page.locator('.survey-container')).to_be_visible(timeout=500)

                question_init = await page.evaluate('window.__INITIAL_STATE__')

                form_data = {}
                for key, value in question_init['QUESTION_DICT'].items():
                    title = value['title']
                    answer = {}

                    prefill_text = text_to_fill.get(title, '-')

                    # 搜索内部的 option
                    for index, option_ele in enumerate(value['option_list']):

                        if '填空' in option_ele['title'] or '日期' in option_ele['title']:

                            option_id = value['option_id_list'][index] + '_open'
                            answer[option_id] = prefill_text

                            print(f"{title} 题目中有一个 填空/日期 题，填写内容：{answer[option_id]}")

                        elif '时' in option_ele['title']:

                            option_id = value['option_id_list'][index] + '_open'
                            answer[option_id] = prefill_text.split(":")[0]

                            print(f"{title} 题目中有一个 小时填空 题，填写内容：{answer[option_id]}")

                        elif '分' in option_ele['title']:

                            option_id = value['option_id_list'][index] + '_open'
                            answer[option_id] = prefill_text.split(":")[1]

                            print(f"{title} 题目中有一个 秒填空 题，填写内容：{answer[option_id]}")

                    # if title != '时间':
                    #     option_id = value['option_id_list'][0] + '_open'
                    #     answer[option_id] = text_to_fill[title]
                    # else:
                    #     option_id0 = value['option_id_list'][0] + '_open'
                    #     option_id1 = value['option_id_list'][1] + '_open'
                    #     answer[option_id0] = text_to_fill[title].split(':')[0]
                    #     answer[option_id1] = text_to_fill[title].split(':')[1]

                    form_data[key] = answer

                t = random.randint(3, 8)
                print(f"大概 {t} 秒 {text_to_fill.get('姓名')}")
                await asyncio.sleep(t)
                await page.evaluate(GET_FORM_BUTTON_CODE, form_data)

                await page.pause()

            except AssertionError:
                err_msg = '未知'
                try:
                    await expect(page.locator('.err-msg')).to_be_visible(timeout=500)
                    err_msg = (await page.locator('.err-msg').text_content()).strip()
                except AssertionError:
                    pass

                print(f"问卷页面未找到：{err_msg}")

                await page.reload(wait_until='domcontentloaded')


async def main():
    with open('./data.json', 'r', encoding='utf-8') as f:
        f = json.load(f)
        results = await asyncio.gather(
            *[wjx(f['url'], d) for d in f['data']]
        )


# 运行
asyncio.run(main())
