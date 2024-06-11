import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def save_csv(variable, save_path):
    """
    保存矩阵为csv文件
    """
    print("Saving... ")
    var = pd.DataFrame(variable)
    var.to_csv(save_path, index=False, header=False)
    print("Done.\n")


def draw_2D(data, longitude=None, latitude=None):
    """
    绘制2D分布图。
    输入相同大小的三个二维矩阵, 经纬度可不填。
    """
    print("Drawing... ")
    plt.figure(figsize=(12, 9))
    if longitude is None and latitude is None:
        plt.imshow(data, cmap='viridis')
        plt.axis('off')
    else:
        plt.pcolormesh(longitude, latitude, data)
        plt.xlabel("longitude")
        plt.ylabel("latitude")
    plt.colorbar(label='Speed (m/s)')
    plt.title('Wind speed distribution')
    print("Done.\n")
    plt.show()


def draw(longitude, latitude, depth_data):
    """
    有错误
    """
    # 创建空白的网格
    grid_size = (np.max(latitude) - np.min(latitude) + 1,
                 np.max(longitude) - np.min(longitude) + 1)
    depth_grid = np.empty(grid_size)
    depth_grid[:] = np.nan  # 将空白网格的值设为NaN

    # 将深度数据填入空白网格中的对应位置
    for i in range(len(latitude)):
        for j in range(len(longitude)):
            depth_grid[latitude[i, j] - np.min(latitude),
                       longitude[i, j] - np.min(longitude)] = depth_data[i, j]

    # 绘制2D彩图
    plt.figure(figsize=(8, 6))
    plt.imshow(depth_grid,
               extent=[
                   np.min(longitude) - 0.5,
                   np.max(longitude) + 0.5,
                   np.min(latitude) - 0.5,
                   np.max(latitude) + 0.5
               ],
               aspect='auto')
    plt.colorbar(label='Depth (m)')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Depth Distribution')
    plt.show()


def tif2excel(tif_file, save_path, max_size=16384):
    """
    tif转为excel。
    尚未优化，别用，电脑会感谢你！
    """
    import rasterio
    print("Reading...")
    with rasterio.open(tif_file) as src:
        x_start = (src.width - max_size) // 2
        y_start = (src.height - max_size) // 2
        num_bands = src.count

        window = rasterio.windows.Window(x_start, y_start, max_size, max_size)
        data = src.read(window=window)
        print("Done.")

        writer = pd.ExcelWriter(save_path)
        for band in range(num_bands):
            print(f"Conversing... ({band+1}/{num_bands})", end='\r')
            df = pd.DataFrame(data[band])
            sheet_name = f'Band_{band+1}'
            df.to_excel(writer,
                        sheet_name=sheet_name,
                        index=False,
                        header=False)
        writer.save()

    print("Done.\nConversion successful.")


def read_block(tif_file: str, size=2000):
    """
    从tif文件中读取块, 返回numpy矩阵。

    参数：
        tif_file: 要读取的tif文件地址。
        size: 读取区块的大小，输入类型为：
                int 从中心取 size * size 大小的块。\n
                [heigth, width] 从中心取 heigth * width 大小的块。\n
                [x, y, heigth, width] 以 (x, y) 为起点取 heigth * width 大小的块。\n
    """
    print("Reading...")

    import rasterio
    with rasterio.open(tif_file) as src:
        total_width = src.width
        total_height = src.height
        if isinstance(size, int):
            if size == -1:
                x_start = y_start = 0
                width = total_width
                height = total_height
            else:
                x_start = (total_width - size) // 2
                y_start = (total_height - size) // 2
                width = height = size
        elif isinstance(size, (list, tuple)):
            width = size[-1]
            height = size[-2]
            if len(size) == 2:
                x_start = (total_width - width) // 2
                y_start = (total_height - height) // 2
            if len(size) == 4:
                x_start = size[0]
                y_start = size[1]

        window = rasterio.windows.Window(x_start, y_start, width, height)

        data = src.read(window=window)
        count = src.count
    print("Done.\n")
    print(f"{count} bands in total. \n"
          f"Total size: {total_height} * {total_width} \n"
          f"Selected size: {height} * {width}\n")
    return data
