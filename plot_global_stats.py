#importing libraries
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.models.annotations import LabelSet
from bokeh.models import ColumnDataSource, Range1d
from bokeh.models import PanTool, WheelZoomTool, BoxZoomTool, ResetTool, HoverTool, SaveTool
from bokeh.models.widgets import Select, Slider
from bokeh.layouts import layout
from bokeh.layouts import gridplot
import pandas as pd
import numpy as np


df = pd.read_csv("country_profile_variables.csv")

df.dropna(inplace=True)

surf_area,gdp,unemp = [],[],[]
for ind in df.index.values:
    try:
        surf_area.append(float(df.loc[ind,"Surface area (km2)"]))
        gdp.append(float(df.loc[ind,"GDP: Gross domestic product (million current US$)"]))
        unemp.append(float(df.loc[ind,'Unemployment (% of labour force)']))
    except:
        df.drop(ind, axis=0, inplace=True)

for i,ue in zip(df.index.values,unemp):
    if (ue < 0):
        df.drop(i, axis=0, inplace=True)
df["Surface area (km2)"]=pd.to_numeric(df["Surface area (km2)"])
df['Population in thousands (2017)']=pd.to_numeric(df['Population in thousands (2017)'])
df["GDP: Gross domestic product (million current US$)"]=pd.to_numeric(df["GDP: Gross domestic product (million current US$)"])
df['Unemployment (% of labour force)']=pd.to_numeric(df['Unemployment (% of labour force)'])


data = {'Population': df['Population in thousands (2017)'].values.tolist(),
        'Population_density': df['Population density (per km2, 2017)'].values.tolist(),
        'GDP': df['GDP: Gross domestic product (million current US$)'].values.tolist(),
        'Surface_area': df['Surface area (km2)'].values.tolist(),
        'country':df['country'].values.tolist(),
        'GDPpercapita':df['GDP per capita (current US$)'].values.tolist(),
        'Unemployment': df['Unemployment (% of labour force)'].values.tolist()}
#crate columndatasource
source_original=ColumnDataSource(data)

source=ColumnDataSource(data)

f = figure(width=1280,height=720)

#create glyphs
f.circle(x="GDP", y="Unemployment", source=source, size=8, fill_alpha=0.6, color='red')

#create filtering function
def filter_pop(attr,old,new):
    source.data={key:[value for i, value in enumerate(source_original.data[key]) if source_original.data["Population"][i]>=slider.value] for key in source_original.data}


slider=Slider(start=min(source_original.data["Population"])-1,end=max(source_original.data["Population"])+1,value=10000,step=10000,title="Population in thousands (2017)")
slider.on_change("value",filter_pop)

f.title.text = "Global Statistics"
f.title.text_color = "black"
f.title.text_font = "times"
f.title.text_font_size = "25px"
f.title.align = "center"
hover = HoverTool(tooltips="""
        <div>
               <div>
                   <span style="font-size: 15px; font-weight: bold;">@country</span>
               </div>
               <div>
                   <span style="font-size: 10px; color: #696;">GDP: Gross domestic product (million current US$): @GDP</span><br>
                   <span style="font-size: 10px; color: #696;">GDP per capita (current US$): @GDPpercapita</span><br>
                   <span style="font-size: 10px; color: #696;">Surface area (km2): @Surface_area</span><br>
                   <span style="font-size: 10px; color: #696;">Population density (per km2, 2017): @Population_density</span>
               </div>
           </div>
   """)

f.tools = [PanTool(),WheelZoomTool(),BoxZoomTool(),ResetTool(),SaveTool()]
f.add_tools(hover)
f.toolbar_location = 'above'
f.toolbar.logo = None
f.xaxis.axis_label = "GDP: Gross domestic product (million current US$)"
f.yaxis.axis_label = "Unemployment (% of labour force)"


#create layout and add to curdoc
# lay_out=layout([[slider]])
lay_out = gridplot([[None, slider]])
curdoc().add_root(f)
curdoc().add_root(lay_out)
