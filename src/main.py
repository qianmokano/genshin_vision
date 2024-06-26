import ReadData
import DrawData

file_path = r'E:\genshin_vision\data\166795667.json'  
save_path = r"E:\genshin_vision\results\results.png"


# 示例调用
data = ReadData.GetData(file_path)  # 从数据文件中读取数据
chr_data, wea_data, common_data, uid = ReadData.SortData(data)  # 对数据进行排序和分类
chr_stat = ReadData.DealData(chr_data)  # 处理角色数据
wea_stat = ReadData.DealData(wea_data)  # 处理武器数据
common_stat = ReadData.DealData(common_data)  # 处理常规物品数据
DrawData.gnrtGachaInfo(chr_stat,wea_stat,common_stat,uid,save_path)