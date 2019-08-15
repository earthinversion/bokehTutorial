from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from random import randrange


p = figure(x_range=(0, 100), y_range=(0, 100))
p.circle(x=50, y=50, radius=15, fill_color=None, line_width=2)

# this is the data source we will stream to
#create columndatasource
source=ColumnDataSource(data=dict(x=[],y=[]))
p.circle(x='x',y='y',size=8,fill_color='red',line_color='black',source=source)

def update():
    new_data=dict(x=[randrange(1,100)],y=[randrange(1,100)])
    source.stream(new_data, rollover=10)

curdoc().add_periodic_callback(update, 1000)
curdoc().add_root(p)