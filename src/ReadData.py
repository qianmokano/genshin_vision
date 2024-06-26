import json
from datetime import datetime

def GetData(file_path: str) :
    """获取文件的 JSON 数据"""
    
    # 打开文件并加载 JSON 数据
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    
    # 打印 JSON 数据，方便调试
    # print(json_data)

    return json_data

def SortData(data: dict) :
    """将数据分类成 角色池 武器池 常驻池 新手池 """

    """获取uid"""
    uid=data["info"]["uid"]

    """初始化"""
    chr_data=[]
    wea_data=[]
    common_data=[]
    # fresh_data={"uid":uid,"list":[]}
    # print(wea_data)

    """根据gacha_type301 302 200 100(角色、武器、常驻、新手) 对数据分类"""
    for single_data in data["list"]:
        # print(single_data)
        if single_data["gacha_type"] == "301" :
            chr_data.append(single_data)
        elif single_data["gacha_type"] == "302" :
            wea_data.append(single_data)
        elif single_data["gacha_type"] == "200" :
            common_data.append(single_data)
        # elif single_data["gacha_type"] == "100" :
        #     fresh_data["list"].append(single_data)
    
    return chr_data , wea_data , common_data ,uid

def DealData(data: dict):
    # 初始化统计数据
    stat = {
        "total": 0,       # 总抽数
        "cntNot5": 0,     # 未出五星抽数
        "cntStar3": 0,    # 三星物品总数
        "cntChr4": 0,     # 四星角色总数
        "cntWea4": 0,     # 四星武器总数
        "cntStar5": 0,    # 五星物品总数
        "star5": [],      # 五星物品列表
        "startTime": None,  # 抽卡记录开始时间
        "endTime": None    # 抽卡记录结束时间
    }
    
    for single_data in data:
        # 统计总抽数
        stat["total"] += 1
        
        # 解析当前条目的时间字符串为 datetime 对象
        currentTime = datetime.strptime(single_data["time"], '%Y-%m-%d %H:%M:%S')
        
        # 更新 startTime 和 endTime
        if stat["startTime"] is None or currentTime < stat["startTime"]:
            stat["startTime"] = currentTime
        if stat["endTime"] is None or currentTime > stat["endTime"]:
            stat["endTime"] = currentTime
            
        # 根据 rank_type 进行分类统计
        if single_data["rank_type"] == "5":
            stat["cntStar5"] += 1
            stat["star5"].append({"name":single_data["name"],"count":stat["cntNot5"]})  # 记录五星物品名称
            stat["cntNot5"] = 0  # 重置未出五星计数
        elif single_data["rank_type"] == "4":
            stat["cntNot5"] += 1
            if single_data["item_type"] == "角色":
                stat["cntChr4"] += 1
            elif single_data["item_type"] == "武器":
                stat["cntWea4"] += 1
        elif single_data["rank_type"] == "3":
            stat["cntNot5"] += 1
            stat["cntStar3"] += 1
    
    # 将 startTime 和 endTime 格式化为 "yyyy.mm.dd hh:mm"
    if stat["startTime"]:
        stat["startTime"] = stat["startTime"].strftime('%Y.%m.%d %H:%M')
    if stat["endTime"]:
        stat["endTime"] = stat["endTime"].strftime('%Y.%m.%d %H:%M')

    return stat


# 示例调用
file_path = r'E:\genshin_vision\data\166795667.json'  # 替换为您的数据文件路径
data = GetData(file_path)
chr_data, wea_data, common_data ,uid = SortData(data)
chr_stat=DealData(chr_data)
wea_stat=DealData(wea_data)
common_stat=DealData(common_data)
# DealData(fresh_data)