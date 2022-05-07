from matplotlib import style
import pygal
from random_walk import RandomWalk

def main():
    rw = RandomWalk()
    rw.fill_walk()
    xyplots = list(zip(rw.x_values,rw.y_values))
    # xy_chart = pygal.XY()
    xy_chart = pygal.XY(stroke = False)
    xy_chart.title = 'Random Walk'
    n = 5
    gap = rw.num_points // 5
    for i in range(n):
        xy_chart.add(f'rw{i}',xyplots[i*gap:(i+1)*gap+1])
    if n*gap<rw.num_points:
        xy_chart.add(f'rw{n+1}',xyplots[n*gap+1:])
    # xy_chart.add('rw',xyplots)
    # xy_chart.render()
    # xy_chart.render_in_browser()
    xy_chart.render_to_file(r'D:\python\2022-05-05\rwpygal_visual1.svg')

def test():
    rw = RandomWalk(10)
    rw.fill_walk()
    xyplots = list(zip(rw.x_values,rw.y_values))
    print(xyplots)

main()
# test()