'''
https://panel.holoviz.org/how_to/editor/editor.html
'''

import panel as pn
import hvplot.pandas
from bokeh.sampledata.autompg import autompg

#choose items for pull-down menu
columns = list(autompg.columns[:-2])

#pull down menu "x"
x = pn.widgets.Select(value='mpg', options=columns, name='x')
#pull down menu "y"
y = pn.widgets.Select(value='hp', options=columns, name='y')
# color picker "color"
color = pn.widgets.ColorPicker(name='Color', value='#AA0505')

#design the layout
pn.Row(
    #left: a column, first a text 2XL size, 
    # then pull down menu x, pull down menu y, color picker 
    pn.Column('## MPG Explorer', x, y, color),
    #right: call a function scatter() with data from: x,y,c
    pn.bind(autompg.hvplot.scatter, x, y, c=color)
    # show() allows to display in VS code
).show()