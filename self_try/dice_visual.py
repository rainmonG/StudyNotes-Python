import pygal
from die import Die

a_die = Die()
b_die = Die()
# c_die = Die()
results=[]
for roll_num in range(50000):
    # result = a_die.roll() + b_die.roll() +c_die.roll()
    result = a_die.roll() * b_die.roll()
    results.append(result)
# print(results)
cases = []
for a in range(1,a_die.num_sides+1):
    for b in range(1,b_die.num_sides+1):
        if a*b not in cases:
            cases.append(a*b)
frequencies = []
for value in cases:
# max_result = a_die.num_sides +b_die.num_sides+c_die.num_sides
# for value in range(3,max_result+1):
    frequency = results.count(value)
    frequencies.append(frequency)
# print(frequecies)
hist = pygal.Bar()
hist.title = 'Results of rolling three D6 die 50000 times.'
hist.x_title = 'Result'
hist.y_title = 'Frequency of Result'
hist.x_labels=map(str,cases)
hist.add('D6 * D6', frequencies) 
# hist.add('D6 + D6 + D6', frequencies) 
hist.render_to_file(r'D:\python\2022-05-05\dice_visual5.svg')