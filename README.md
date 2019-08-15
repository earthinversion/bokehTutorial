# Bokeh Tutorial for beginners

## Installation:
Install all the libraries using conda in a separate environment:

`conda env create -f environment.yml`

## Topics Covered:
1. Setting the dimension of the figure and plotting markers
2. Styling the markers and the figure background
3. Setting and styling the title of the figure
4. Styling the axes of the figure
5. Styling the grid and legends
6. Introduction to ColumnDataSource
7. Configuring toolbars for the plot
8. Bokeh layouts - column, row, gridplot
9. Bokeh widgets - Tabs, Panel
10. Selecting data points in the bokeh figure

## Real World Examples
Other than the basic introduction, this tutorial includes two examples:
1. Plot of the Earthquake events (the event information are obtained using the FDSN service from Obspy package)

`python EQviz.py` for the plot without widgets

`bokeh serve EQviz_with_widgets.py` for plot with the input box for the starting and end year for the search of events. This is quite slow as the program need to request data using the Obspy method each time.


2. Interactive plot of the global population statistics. Introduction of the slider widget. The widgets can be similarly implemented. To execute this program, you need to run it on the bokeh server using the command:

`bokeh serve plot_global_stats.py`

3. Streaming random data: randomly plot 10 circles glyphs.

`bokeh serve streaming_data.py`