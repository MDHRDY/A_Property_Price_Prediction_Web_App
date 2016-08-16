from flask import Flask, render_template, request, redirect
import pandas as pd
from bokeh.embed import components 
from bokeh.plotting import figure, output_file, show
from bokeh.io import output_notebook, show
from bokeh.charts import Scatter
import jinja2
from IPython.display import HTML
import numpy as np

from bokeh.io import output_file, show
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d, PanTool, WheelZoomTool, BoxSelectTool
)



app = Flask(__name__, static_url_path = "", static_folder = "")

app.vars={}

@app.route('/graph', methods=['GET','POST'])
@app.route('/', methods=['GET','POST'])
def generate_graph():
	map_options = GMapOptions(lat=40.699389, lng=-73.955454, map_type="roadmap", zoom=10)
	
	plot = GMapPlot(
    x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, title="NYC"
	)
	
	df = pd.read_csv('heroku_test.csv', low_memory=False)
	df2 = pd.read_csv('Loss_of_Over50percent.csv', low_memory=False)
	source = ColumnDataSource(
    	data = dict(
        	lat = np.array(df.Lat),
        	lon = np.array(df.Long),
    	)
	)
	source2 = ColumnDataSource(
    	data = dict(
        	lat = np.array(df2.Lat),
        	lon = np.array(df2.Long),
    	)
	)	
	circle = Circle(x="lon", y="lat", size=2, fill_color="red", fill_alpha=0.8, line_color=None)
	plot.add_glyph(source, circle)
	#circle2 = Circle(x="lon", y="lat", size=2, fill_color="blue", fill_alpha=0.8, line_color=None)
	#plot.add_glyph(source2, circle2)
	plot.add_tools(PanTool(), WheelZoomTool())
	script, div = components(plot)
	return render_template('graph.html', script=script, div=div)


@app.route('/Page2', methods=['GET','POST'])
def generate_graph2():
	map_options3 = GMapOptions(lat=40.652389, lng=-73.965454, map_type="roadmap", zoom=11)
	
	plot3 = GMapPlot(
    x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options3, title="NYC"
	)
	
	df3 = pd.read_csv('lst_yr_up_25percent_from50percentup_subset.csv', low_memory=False)
	source3 = ColumnDataSource(
    	data = dict(
        	lat3 = np.array(df3.Lat),
        	lon3 = np.array(df3.Long),
    	)
	)
	circle3 = Circle(x="lon3", y="lat3", size=5, fill_color="red", fill_alpha=0.8, line_color=None)
	plot3.add_glyph(source3, circle3)
	plot3.add_tools(PanTool(), WheelZoomTool())
	script, div = components(plot3)
	
	return render_template('Page2.html', script=script, div=div)




@app.errorhandler(500)
def pageNotFound(error):
	return render_template('error_page.html')

  
@app.errorhandler(404)
def pageNotFound(error):
	return render_template('error_page.html')


if __name__ == "__main__":
    app.run(debug=True)
    