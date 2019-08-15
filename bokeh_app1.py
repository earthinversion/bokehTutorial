from numpy.random import random

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.plotting import ColumnDataSource, Figure
from bokeh.models.widgets import Select, TextInput


def get_data(N):
    return dict(x=random(size=N), y=random(size=N), r=random(size=N) * 0.03)


source = ColumnDataSource(data=get_data(200))


p = Figure(tools="", toolbar_location=None)
r = p.circle(x='x', y='y', radius='r', source=source,
             color="navy", alpha=0.6, line_color="white")


COLORS = ["black", "firebrick", "navy", "olive", "goldenrod"]
select = Select(title="Color", value="navy", options=COLORS)
input  = TextInput(title="Number of points", value="200")


def update_color(attrname, old, new):
    r.glyph.fill_color = select.value
select.on_change('value', update_color)

def update_points(attrname, old, new):
    N = int(input.value)
    source.data = get_data(N)
input.on_change('value', update_points)


layout = column(row(select, input, width=400), row(p))
curdoc().add_root(layout)