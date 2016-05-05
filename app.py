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
def generate_graph():
	map_options = GMapOptions(lat=40.699389, lng=-73.955454, map_type="roadmap", zoom=10)
	
	plot = GMapPlot(
    x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, title="NYC"
	)
	
	df = pd.read_csv('Over60percent_apprec.csv', low_memory=False)
	#la = np.array(df.Lat) 
	#lo = np.array(df.Long)
	source = ColumnDataSource(
    	data = dict(
        	lat = np.array(df.Lat),
        	lon = np.array(df.Long),
    	)
	)
	circle = Circle(x="lon", y="lat", size=2, fill_color="blue", fill_alpha=0.8, line_color=None)
	plot.add_glyph(source, circle)
	plot.add_tools(PanTool(), WheelZoomTool())
	#output_file("gmap_plot.html")
	#show(plot)
	script, div = components(plot)
	return render_template('graph.html', script=script, div=div)


@app.errorhandler(500)
def pageNotFound(error):
	return render_template('error_page.html')

  
@app.errorhandler(404)
def pageNotFound(error):
	return render_template('error_page.html')


if __name__ == "__main__":
    app.run(debug=True)
    