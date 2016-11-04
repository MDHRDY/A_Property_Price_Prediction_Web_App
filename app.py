from flask import Flask, render_template, request, redirect
import pandas as pd
import numpy as np
import dill
import jinja2
import urllib, json
from bokeh.embed import components 
from bokeh.plotting import figure, output_file, show
from bokeh.io import output_notebook, show
from bokeh.charts import Scatter
from bokeh.models import (
	GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d,
	PanTool, WheelZoomTool, BoxSelectTool )

with open("dills/df_2013_14_nd_15.dill", "r") as f:
    df = dill.load(f)    
with open("dills/price_pred_lat_long_function.dill", "r") as f2:
    conv_coord_for_price_model = dill.load(f2)
with open("dills/unsupervised_cluster_10_1_post_sklearn18_update.dill", "r") as f3:
    model = dill.load(f3)
with open("dills/Xs.dill", "r") as f4:
    Xs = dill.load(f4)   
with open("dills/within_20_half_of_time.dill", "r") as f5:
    price_model = dill.load(f5) 
    

google_api = "https://maps.googleapis.com/maps/api/geocode/json?address="
key = 'NY&key=AIzaSyA8VBsATdqaQZforSrLl88rW2Kr-fYGHjo'
key2 = "AIzaSyBkuO8yMgbJ3RfHtCfUOT3aLHlhX3HkQsQ&"


app = Flask(__name__, static_url_path = "", static_folder = "")
app.vars={}

@app.route('/', methods=['GET','POST'])
@app.route('/nycProperty.html',methods=['GET','POST'])  
@app.route('/nycProperty_intro.html',methods=['GET','POST'])  
def generate_main():
    locations = [40.715, -74.006] * 10 
    dict = [[40.715, -74.006,
    	'Enter an address in the search bar above to obtain details.', 2015, 0]
 					for _ in xrange(9)]   
    map_lat = 40.83; map_long = -73.99 

    if request.method == 'GET':
    	return render_template('nycProperty_intro.html', num = locations, 
    				center_lat= map_lat, center_long=map_long, zoom=13, 
    				d=dict, length=1,key2=key2) 
    else:
    	app.vars['name'] = request.form['address']

    	if app.vars['name'] == '':
    			return render_template('nycProperty_intro.html', num = locations, 
    				center_lat= map_lat, center_long=map_long,zoom=13, d=dict, 
    				length=1,key2=key2) 
    	else:
    		try:
    			full_address = app.vars['name'].split(',')
    			format_address = full_address[0] + ', ' + full_address[1]
    			user_input = format_address.replace(' ', '+')
    			url = google_api + user_input + key
    			response = urllib.urlopen(url)
    			
    			data = json.loads(response.read())
    			d =  data['results'][0]['geometry']['location']
    			address = data['results'][0]['address_components'][0]['long_name'] + \
    				' ' + data['results'][0]['address_components'][1]['long_name']
    			Lat_Long = str(d['lat']) + ', ' + str(d['lng'])
    			full_address = data['results'][0]['formatted_address'].split(',')
    			zipcode = full_address[(len(full_address)-2)].split()[1]
    			borough = data['results'][0]['address_components'][3]['long_name']
    			address_details = [Lat_Long, zipcode, borough, address] 
    			
    			Lt_Lg = model.get_model_values(d['lat'], d['lng'])
    			neighbors = model.transform(np.array(Lt_Lg).reshape(1, -1))[1][0]
    			master_coord = []; d2 = []; j=0
    			for i in neighbors:
    				temp = []
    				temp.append( df.iloc[i,106:107][0] )
    				temp.append( df.iloc[i,105:106][0] )
    				temp.append( df.iloc[i,8:9][0] )
    				temp.append( df.iloc[i,107:108][0] )
    				temp.append( df.iloc[i,19:20][0] )
    				temp.append( df.iloc[i,11:12][0] )
    				temp.append( df.iloc[i,15:16][0] )
    				temp.append( df.iloc[i,16:17][0] )    				
    				Lt = Xs.iloc[i:i+1,0]; Lg = Xs.iloc[i:i+1,1]
    				inst = model.get_lat_long(Lt,Lg)
    				master_coord.append( float(inst[0]) )
    				master_coord.append( float(inst[1]) )
    				
    				d2.append(temp) 
    				dict[j] = temp
    				j += 1
    			locations = master_coord
    			price_lat_long = conv_coord_for_price_model(d['lat'],d['lng'])
    			if borough == 'Brooklyn':
    				sample = np.array([price_lat_long[0],price_lat_long[1],1,0,0,0,0,1,0,0])
    			elif borough == 'Manhattan':
    				sample = np.array([price_lat_long[0],price_lat_long[1],0,0,0,0,1,1,0,0])
    			elif borough == 'Queens':
    			    sample = np.array([price_lat_long[0],price_lat_long[1],0,1,0,0,0,1,0,0])
    			elif borough == 'Bronx':
    			    sample = np.array([price_lat_long[0],price_lat_long[1],0,0,0,1,0,1,0,0])
    			else:
    			    sample = np.array([price_lat_long[0],price_lat_long[1],0,0,1,0,0,1,0,0])
    			
    			predicted_value = int(price_model.predict(sample.reshape(1,-1))[0])
    			
    			return render_template('nycProperty_pred.html', num = master_coord, 
    				center_lat= master_coord[0], center_long=master_coord[1],zoom=15, 
    				d=d2, length=8, LatLong=address_details,key2=key2, 
    				price_prediction=predicted_value) 
    		except:
    			respond_w ="Oops! Couldn't find that address, or encountered an unknown \
    					 problem. Please use the autocomplete feature and confirm that \
    					 the address is located within New York City."
    			return render_template('nycProperty_ex.html', num = locations, 
    				center_lat= map_lat, center_long=map_long, zoom=13, d=dict, length=1, 
    				respond=respond_w, key2=key2)  

# Google maps Fig w/ red/blue classified properties
@app.route('/graph.html', methods=['GET','POST'])
@app.route('/graph', methods=['GET','POST'])
def graph():
	map_options = GMapOptions(lat=40.699389, lng=-73.955454, map_type="roadmap", zoom=10)
	
	plot = GMapPlot(
    x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, title="NYC"
	)
	
	df = pd.read_csv('csvs/Over60percent_apprec.csv', low_memory=False)
	source = ColumnDataSource(
    	data = dict(
        	lat = np.array(df.Lat),
        	lon = np.array(df.Long),
    	)
	)
	circle = Circle(x="lon", y="lat", size=2.5, fill_color="red", 
						fill_alpha=0.8, line_color=None)
	plot.add_glyph(source, circle)
	
	
	df2 = pd.read_csv('csvs/Loss_of_Over60percent.csv', low_memory=False)
	source2 = ColumnDataSource(
    	data = dict(
        	lat = np.array(df2.Lat),
        	lon = np.array(df2.Long),
    	)
	)	
	circle2 = Circle(x="lon", y="lat", size=2.5, fill_color="blue", 
						fill_alpha=0.8, line_color=None)
	plot.add_glyph(source2, circle2)
	
	plot.add_tools(PanTool(), WheelZoomTool())
	script, div = components(plot)
	return render_template('graph.html', script=script, div=div)


@app.route('/heat_map', methods=['GET','POST'])
@app.route('/heat_map.html', methods=['GET','POST'])
def heat_map():
    if request.method == 'GET':
    	return render_template('heat_map.html')  
    else:
    	return render_template('heat_map.html') 

@app.route('/zillow.html', methods=['GET','POST'])
def zillow():
    if request.method == 'GET':
    	return render_template('nycProperty_zillow.html')  
    else:
    	return render_template('nycProperty_zillow.html') 


if __name__ == "__main__":
    app.run()
    