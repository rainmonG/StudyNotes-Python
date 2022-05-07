import pygal
from die import Die

a_die = Die()
results=[]
for roll_num in range(1000):
    result = a_die.roll()
    results.append(result)
# print(results)
frequencies = []
for value in range(1,a_die.num_sides+1):
    frequency = results.count(value)
    frequencies.append(frequency)
# print(frequecies)
hist = pygal.Bar()
hist.title = 'Results of rolling one D6 1000 times.'
hist.x_title = 'Results'
hist.y_title = 'Frequency of Result'
hist.x_labels=map(str,[1,2,3,4,5,6])
hist.add('D6', frequencies) 
hist.render_to_file(r'D:\python\2022-05-05\die_visual.svg')