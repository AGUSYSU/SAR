from model import CMOD
import numpy as np
from src import func

tif_file = r"E:\大创\SAR风能评估\data\dealed\subset_S1_20230828_Malaxiya_spk.tif"

# 读取数据，size 可以为 int、 list、 tuple 类型，详见函数注释
# data 为形状 [band count, height, width] 的矩阵
data = func.read_tif(tif_file, size=[5000, 5000, 5000, 5000])

# 顺序为snap导出时波段的顺序
sigma0 = data[0]
latitude = data[1]
longitude = data[2]
inc = data[3]

# 角度制
phi = np.ones(sigma0.shape) * 0
# filter = filter.Filter()

model = CMOD.CMOD5_N()
v = model.inverse(sigma0_obs=sigma0, phi=phi, incidence=inc, iterations=10)

# 保存变量数据
# func.save_csv(v, "./data/v.csv")

# 画图， 经纬度、保存路径可以省略
func.draw_2D(v, longitude, latitude, save_path="./data/CMOD5_N.png")
