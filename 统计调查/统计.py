import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import matplotlib.font_manager as fm


# 读取CSV文件
file_path = './结果.csv'
data = pd.read_csv(file_path, on_bad_lines='skip')


# 注册并设置全局中文字体
font_path = './ALIBABAPUHUITI-3-105-HEAVY.TTF'
font_prop = fm.FontProperties(fname=font_path)
fm.fontManager.addfont(font_path)
plt.rcParams['font.sans-serif'] = [font_prop.get_name()]
plt.rcParams['axes.unicode_minus'] = False  # 用于正常显示负号

# 统计年龄、职业和教育背景的分布
age_distribution = data['1'].value_counts()
profession_distribution = data['2'].value_counts()
education_distribution = data['3'].value_counts()

# 绘制年龄、职业和教育背景的饼状图
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# 年龄分布
axes[0].pie(age_distribution, labels=age_distribution.index, autopct='%1.1f%%', startangle=90)
axes[0].set_title('年龄分布', fontproperties=font_prop)

# 职业/身份分布
axes[1].pie(profession_distribution, labels=profession_distribution.index, autopct='%1.1f%%', startangle=90)
axes[1].set_title('职业/身份分布', fontproperties=font_prop)

# 教育背景分布
axes[2].pie(education_distribution, labels=education_distribution.index, autopct='%1.1f%%', startangle=90)
axes[2].set_title('教育背景分布', fontproperties=font_prop)

plt.tight_layout()
plt.show()

# 处理“了解AI的渠道”数据（多选题）
channel_data = data['6'].dropna().str.split(';', expand=True).stack().value_counts()


# 绘制了解AI的渠道条形图
plt.figure(figsize=(10, 6))
y_pos = range(len(channel_data))
colors = sns.color_palette('Blues_d', len(channel_data))  # 用 seaborn 取色，但画图用 matplotlib
plt.barh(y_pos, channel_data.values, color=colors)
plt.yticks(y_pos, channel_data.index, fontproperties=font_prop)
plt.title('了解AI的渠道分布', fontproperties=font_prop)
plt.xlabel('人数', fontproperties=font_prop)
plt.ylabel('渠道', fontproperties=font_prop)
plt.gca().invert_yaxis()  # 可选：让最大值在顶部
plt.show()

# 生成“AI发展的最大期待是什么”词云
expectations = data['21'].dropna().str.cat(sep=' ')
wordcloud = WordCloud(font_path=font_path, width=800, height=400, background_color='white').generate(expectations)

# 显示词云
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('AI发展的最大期待 - 词云', fontproperties=font_prop)
plt.show()

