#import libraries
import geopandas as gpd
import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.tile_providers import get_provider, Vendors
from bokeh.models import ColumnDataSource, PanTool, WheelZoomTool, BoxZoomTool, ResetTool, HoverTool, SaveTool
import numpy as np
from extract_eq_info import extract_eq_info
from merc_proj import LongLat_to_EN
from bokeh.models.widgets import Select, TextInput
from bokeh.layouts import column, row
from bokeh.io import curdoc


tile_provider = get_provider(Vendors.CARTODBPOSITRON_RETINA)

def update_data(starttime,endtime):
    years,juldays,latitudes,longitudes,depths,magnitudes,magnitude_type,event_text,eq_time=extract_eq_info(starttime=starttime,endtime=endtime,minmagnitude=6)

    years,juldays,latitudes,longitudes,depths,magnitudes,magnitude_type=np.array(years),np.array(juldays),np.array(latitudes),np.array(longitudes),np.array(depths),np.array(magnitudes),np.array(magnitude_type)

    ## Plotting data
    data = {'years':years,
    'juldays':juldays,
    'latitudes':latitudes,
    'longitudes':longitudes,
    'magnitudes':magnitudes,
    'depths':depths,
    'magnitude_type':magnitude_type,
    'event_text':event_text,
    'event_time':eq_time}

    df=pd.DataFrame.from_dict(data)
    df['E'], df['N'] = zip(*df.apply(lambda x: LongLat_to_EN(x['longitudes'], x['latitudes']), axis=1))
    df_shallow = df[df['depths']<100]
    df_middle = df[(df['depths']>=100) & (df['depths']<300)]
    df_deep = df[df['depths']>=300]
    eq_info_shallow = ColumnDataSource(df_shallow)
    eq_info_middle = ColumnDataSource(df_middle)
    eq_info_deep = ColumnDataSource(df_deep)
    return (eq_info_shallow,eq_info_middle,eq_info_deep)


## range bounds supplied in web mercator coordinates
x_range, y_range =  ((-18706892.5544, 21289852.6142), (-7631472.9040, 12797393.0236))

p = figure(width=1280,height=720, x_range=x_range, y_range=y_range)

## Styling
p.add_tile(tile_provider)
p.tools = [PanTool(),WheelZoomTool(),BoxZoomTool(),ResetTool(),SaveTool()]
hover = HoverTool(tooltips="""
     <div>
            <div>
                <span style="font-size: 12px; font-weight: bold;">@event_text</span>
            </div>
            <div>
                <span style="font-size: 10px; color: #696;">Event time: @event_time</span><br>
                <span style="font-size: 10px; color: #696;">Coordinates: (@longitudes,@latitudes)</span><br>
                <span style="font-size: 10px; color: #696;">Magnitude: @magnitudes @magnitude_type</span><br>
                <span style="font-size: 10px; color: #696;">Depth: @depths km</span>
            </div>
        </div>
""")
p.add_tools(hover)
p.toolbar_location = 'above'
p.toolbar.logo = None



st_year = "2002"
end_year="2002"
eq_info_shallow,eq_info_middle,eq_info_deep=update_data("{}-01-01".format(st_year),"{}-01-02".format(end_year))

p.circle(x="E", y="N", size='magnitudes', fill_alpha=0.2, color='blue', legend='Shallow Earthquakes (<100km)', source=eq_info_shallow)
p.circle(x="E", y="N", size='magnitudes', fill_alpha=0.2, color='green', legend='Intermediate Earthquakes (100-300 km)', source=eq_info_middle)
p.circle(x="E", y="N", size='magnitudes', fill_alpha=0.2, color='red', legend='Deep Earthquakes (>300 km)', source=eq_info_deep)



## Legend 
p.legend.location = 'bottom_left'
p.legend.background_fill_color = 'white'
p.legend.background_fill_alpha = 0.9
p.legend.click_policy='hide'
p.xaxis.visible = False
p.yaxis.visible = False
input  = TextInput(title="Starting and End Year (e.g: 2000,2001)", value="2000,2001")
def update_year(attrname, old, new):
    st_year,end_year = input.value.split(",")
    print(st_year,end_year)
    st_year = int(st_year)
    end_year = int(end_year)
    eq_info_shallow,eq_info_middle,eq_info_deep=update_data("{}-01-01".format(st_year),"{}-01-02".format(end_year))
    print('Data retrieved')
input.on_change('value', update_year)


layout = column(row(input, width=400), row(p))
curdoc().add_root(layout)
