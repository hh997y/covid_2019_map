import json
import requests
import time
import pandas as pd

URL = "https://gwpre.sina.cn/interface/fymap2020_data.json?random=0.7906952201023671&_=%s" % int(time.time() * 1000)

# 获取网页响应
resp = requests.get(URL)
# 解析网页响应内容（Unicode编码）
content = resp.content.decode("unicode_escape")
# 将网页内容改为 json 格式
con_json = json.loads(content)

# print(con_json["data"]["worldlist"])

china_data = con_json["data"]["list"]
china_list = []
for i in range(len(china_data)):
    province = china_data[i]['name']  # 省名
    total = china_data[i]['value']
    death = china_data[i]['deathNum']
    china_dict = {}
    china_dict['province'] = province
    china_dict['value'] = int(total)
    china_dict["death"] = int(death)
    china_list.append(china_dict)
china_data = pd.DataFrame(china_list).sort_values(by="value",ascending=False).reset_index().drop(['index'], axis=1)
print(china_data)

global_data = pd.DataFrame(con_json["data"]["worldlist"])
global_data = global_data[["name","value","deathNum"]]
for i in range(len(global_data)):
    global_data.loc[i, 'value'] = int(global_data.loc[i, 'value'])
    global_data.loc[i, 'deathNum'] = int(global_data.loc[i, 'deathNum'])
a = []
for i in range(len(global_data)):
    a.append(global_data.loc[i,'name'])
world_name = pd.read_excel("世界各国中英文对照.xlsx")
global_data = pd.merge(world_name,global_data,left_on = "中文",right_on = "name",how="inner")
global_data = global_data[["中文","英文","value","deathNum"]].sort_values(by="value",ascending=False).reset_index().drop(['index'], axis=1)
#####打印世界数据
print(' ')
c = 0
print('{:<9}{:<9}{:<9}{:<9}'.format(' ', '中文', 'value', 'deathNum'))
for i in range(len(global_data)):
    print('{:<9}{:<9}{:<9}{:<9}'.format(c, global_data.loc[i, '中文'], global_data.loc[i, 'value'], global_data.loc[i, 'deathNum']))
    c += 1
#####
#####全球总数
res, dres = 0, 0
for i in range(len(global_data)):
    res += global_data.loc[i,'value']
    dres += global_data.loc[i,'deathNum']
print("全球确诊总数：{}， 全球死亡总数：{}".format(res, dres))
#####
#####检查是否翻译对了
print(' ')
b = []
for i in range(len(global_data)):
    b.append(global_data.loc[i,'中文'])
f = 0
for i in a:
    if i not in b:
        f = 1
        print(i)
if f == 0:
    print('all in')
#####

# # pandas
# print(china_data.columns.values)  # 打印columns值
# print(china_data.index.values)  # 打印index值
# for i in range(len(china_data)):
#     if china_data.loc[i,'province']=="四川":
#         sc = china_data.loc[[i]]
#         # print(sc["city"],sc["total"])
# print(china_data.loc[[0]])  # loc打印某一行的值，某一列直接china_data[]



from pyecharts.charts import * #导入所有图表
from pyecharts import options as opts
#导入pyecharts的主题（如果不使用可以跳过）
from pyecharts.globals import ThemeType

# # 全球疫情热图
world_map = Map(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS,width="900px",height="580px"))
world_map.add("总计",[list(z) for z in zip(list(global_data["英文"]), list(global_data["value"]))], "world",is_map_symbol_show=False)
world_map.set_global_opts(title_opts=opts.TitleOpts(title="2019_nCoV-世界疫情地图"),
                          visualmap_opts=opts.VisualMapOpts(is_piecewise=True,
                        pieces=[
                                {"min": 10001 , "label": '>10000',"color": "#2F0000"}, #不指定 max，表示 max 为无限大
                                {"min": 1001, "max": 10000, "label": '1001-10000', "color": "#893448"},
                                {"min": 500, "max": 1000, "label": '501-1000',"color": "#ff585e"},
                                {"min": 101, "max": 499, "label": '101-500',"color": "#fb8146"},
                                {"min": 10, "max": 100, "label": '11-100',"color": "#ffb248"},
                                {"min": 0, "max": 9, "label": '0-10',"color": "#fff2d1"}]))
world_map.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
# world_map.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
# print(world_map.render_notebook())

# 中国热图
# 数据处理
area_data = china_data[["province","value"]]
area_map = Map(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS,width="900px",height="590px"))

a = [list(z) for z in zip(list(area_data["province"]), list(area_data["value"]))]
area_map.add("总计", a, "china",is_map_symbol_show=False)

area_map.set_global_opts(title_opts=opts.TitleOpts(title="2019_nCoV中国疫情地图"),visualmap_opts=opts.VisualMapOpts(is_piecewise=True,
                pieces = [
                        {"min": 10001 , "label": '>10000',"color": "#2F0000"}, #不指定 max，表示 max 为无限大
                        {"min": 1001 , "max": 10000, "label": '1001-10000',"color": "#893448"},
                        {"min": 500, "max": 1000, "label": '501-1000',"color": "#ff585e"},
                        {"min": 101, "max": 499, "label": '101-500',"color": "#fb8146"},
                        {"min": 10, "max": 100, "label": '11-100',"color": "#ffb248"},
                        {"min": 0, "max": 9, "label": '0-10',"color" : "#fff2d1" }]))

area_map.set_series_opts(label_opts=opts.LabelOpts(is_show=True))
area_map.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))  # a:总计 b：省名 c：数据

page = Page()
page.add(world_map)
page.add(area_map)
path=u'C:\\Users\\38969\\Desktop\\2019_nCoV 可视化.html'
page.render(path)