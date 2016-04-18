from flask import Flask, render_template, request, redirect
import pandas as pd
from bokeh.embed import components 
from bokeh.plotting import figure, output_file, show
from bokeh.io import output_notebook, show
from bokeh.charts import Scatter
import jinja2
from IPython.display import HTML
import numpy as np
import matplotlib.pyplot as plt




app = Flask(__name__, static_url_path = "", static_folder = "")

app.vars={}


@app.route('/graph', methods=['GET','POST'])
def generate_graph():
	df = pd.read_csv('For_Regression.csv')
	xval = df['Latitude'].tolist()
	yval = df['Longitude'].tolist()
	plot = figure(width=500, height=500,title='Brooklyn Property Listings')
	plot.yaxis.axis_label = "Latitude"
	plot.xaxis.axis_label = "Longitude"

	plot.scatter(yval,xval)
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
    