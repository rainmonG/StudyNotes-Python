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
    xy_chart.show_legend = False
    for xyplot in xyplots:
        xy_chart.add(f'{xyplot}',(xyplot,))
    # xy_chart.add('rw',xyplots)
    # xy_chart.render()
    # xy_chart.render_in_browser()
    xy_chart.render_to_file(r'D:\python\2022-05-05\rwpygal_visual2.svg')

def test():
    rw = RandomWalk()
    rw.fill_walk()
    xyplots0 = list(zip(rw.x_values,rw.y_values))
    xyplots = xyplots0[:10]
    # print(xyplots)
    xy_chart = pygal.XY(stroke = False)
    xy_chart.title = 'Random Walk'
    xy_chart.show_legend = False
    for xyplot in xyplots:
        xy_chart.add('',(xyplot,))
    xy_chart.render_to_file(r'D:\python\2022-05-05\test_xy1.svg')

main()
# test()