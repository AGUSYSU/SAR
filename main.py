from model import CMOD
import numpy as np
from src import func, filter

# 文件路径
tif_file = r"subset.tif"

# 读取数据，size 可以为 int、 list、 tuple 类型，详见函数注释
# data 为形状 [band count, height, width] 的矩阵
data = func.read_tif(tif_file, size=-1)

# 顺序为snap导出时波段的顺序
sigma0 = data[0]
latitude = data[1]
longitude = data[2]
inc = data[3]
phi = np.ones(sigma0.shape) * 0

# 滤波器
Filter = filter.Filter()


model = CMOD.CMOD5_N()
v = model.inverse(sigma0_obs=sigma0, phi=phi, incidence=inc, iterations=10)

# 画图， 经纬度、保存路径可以省略
func.draw_2D(v, longitude, latitude, "data/CMOD5_N.png")
