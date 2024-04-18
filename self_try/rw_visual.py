import matplotlib.pyplot as plt
from random_walk import RandomWalk

while True:
    rw = RandomWalk()
    rw.fill_walk()
    # 设置绘图窗口的尺寸，要在画图前设置
    plt.figure(figsize=(10, 6))

    plt.scatter(rw.x_values,rw.y_values,
        c= range(rw.num_points),cmap='PuBu',s=1)
    # plt.plot(rw.x_values,rw.y_values,linewidth=1,c=(1,0.6,0.7))

    # plt.axis('off')  
    # plt.xticks([])
    # plt.yticks([])
    
    plt.show()

    keep_running = input('Make another walk?(y/n): ')
    if keep_running == 'n':
        break