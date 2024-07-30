import matplotlib.pyplot as plt
import numpy as np
from multiprocessing import Pool

fig, ax = plt.subplots(figsize=(12, 6))

def generate_data(i):
    y = i + 5
    x = [x + i for x in range(6)]
    return x, y

if __name__ == '__main__':
    # 使用进程池执行并行任务
    with Pool(processes=10) as pool:
        results = pool.map(generate_data, range(10))

    # 在主进程中绘制数据
    for x, y in results:
        ax.plot(x, np.full_like(x, y), 'r.')

    plt.axis("equal")
    plt.show()