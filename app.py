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
#from IPython.display import HTML

with open("df_2013_14_nd_15.dill", "r") as f:
    df = dill.load(f)    
with open("price_pred_lat_long_function.dill", "r") as f9:
    conv_coord_for_price_model = dill.load(f9)
#with open("kd_tree_8to98.dill", "r") as f:
#    sgd = dill.load(f)
#with open("lat_long.dill", "r") as f3:
#    lat_long_model = dill.load(f3) 


# pre sklearn 0.18 update - now deprecated. 
# 3 issues:
# A) need to reshape input w/ (.reshape(1,-1) - this still works
# B) warned about cross-validation, which is now deprecated
# C) problem using 0.18 sklearn w/ dill model from pre-0.18 version   
#with open("model_9_26.dill", "r") as f4:
#    model = dill.load(f4) 
with open("unsupervised_cluster_10_1_post_sklearn18_update.dill", "r") as f4:
    model = dill.load(f4)

with open("Xs.dill", "r") as f5:
    Xs = dill.load(f5)  
  
with open("within_20_half_of_time.dill", "r") as f7:
    price_model = dill.load(f7) 
    
#with open("conv_coord.dill", "r") as f6:
#    conv_coord = dill.load(f6) 

google_api = "https://maps.googleapis.com/maps/api/geocode/json?address="
key = 'NY&key=AIzaSyA8VBsATdqaQZforSrLl88rW2Kr-fYGHjo'



app = Flask(__name__, static_url_path = "", static_folder = "")
app.vars={}

@app.route('/', methods=['GET','POST'])
@app.route('/graph', methods=['GET','POST'])
@app.route('/nycProperty.html',methods=['GET','POST'])
@app.route('/nycProperty_auto.html',methods=['GET','POST'])
def generate_graph():
    nquestions = [40.715, -74.006] * 10 #, 'Enter an address', 'in the seach field above', 'to get map results']
    dict = []
    dict = [[40.715, -74.006,'Enter an address in the search bar above to obtain details.', 2015, 0],[0,1,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    if request.method == 'GET':
    	map_lat = 40.83 #return_coord[0]
    	map_long = -73.99 #return_coord[1]
    	
    	return render_template('nycProperty_intro.html', num = nquestions, center_lat= map_lat, center_long=map_long, zoom=13, d=dict, length=1) #, map_lat_center = map_lat, map_long_center = map_long)
    else:
    	app.vars['name'] = request.form['address']

    	if app.vars['name'] == '':
    			map_lat = 40.83 #return_coord[0]
    			map_long = -73.99 #return_coord[1]
    			return render_template('nycProperty_intro.html', num = nquestions, center_lat= map_lat, center_long=map_long,zoom=14, d=dict, length=1) #, map_lat_center = map_lat, map_long_center = map_long)

    		#return render_template('nycProperty_auto.html', num = '') #,map_lat_center = 40.8383885679, map_long_center = -73.9027923602)
    	else:
    		try:
    			full_address = app.vars['name'].split(',')
    			format_address = full_address[0] + ', ' + full_address[1]
    			user_input = format_address.replace(' ', '+')
    			url = google_api + user_input + key
    			response = urllib.urlopen(url)
    			
    			data = json.loads(response.read())
    			d =  data['results'][0]['geometry']['location']
    			address = data['results'][0]['address_components'][0]['long_name'] + ' ' + \
    					data['results'][0]['address_components'][1]['long_name']
    			Lat_Long = str(d['lat']) + ', ' + str(d['lng'])
    			full_address = data['results'][0]['formatted_address'].split(',')
    			zipcode = full_address[(len(full_address)-2)].split()[1]
    			borough = data['results'][0]['address_components'][3]['long_name']
    			address_details = [Lat_Long, zipcode, borough, address] #, zip, borough]
    			
    			Lt_Lg = model.get_model_values(d['lat'], d['lng'])
    			#borough = data[data['results'][0]['address_components'][3]['long_name']
    			neighbors = model.transform(np.array(Lt_Lg).reshape(1, -1))[1][0]
    			master_coord = []
    			d2 = []
    			j=0
    			#dict[j] = 
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
    				Lt = Xs.iloc[i:i+1,0]
    				Lg = Xs.iloc[i:i+1,1]
    				
    				inst = model.get_lat_long(Lt,Lg)
    				master_coord.append( float(inst[0]) )
    				master_coord.append( float(inst[1]) )
    				
    				d2.append(temp) #[Lt,Lg, inst[0], inst[1] ]
    				dict[j] = temp
    				j += 1
    			#nquestions = 'Results for: ' + format_address + ', coordinates: ' + str(neighbors) + 'check'#str( prediction ) + ' \n' + Lat_Long #return_coord[0])
    			nquestions = master_coord
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
				#model.predict(sample.reshape(1,-1))[0]
    			predicted_value = int(price_model.predict(sample.reshape(1,-1))[0])
    			return render_template('nycProperty_pred.html', num = master_coord, center_lat= master_coord[0], center_long= master_coord[1], zoom=14, d=d2, length=8, LatLong=address_details, price_prediction=predicted_value)#, borough=borough) #, map_lat_center = map_lat, map_long_center = map_long)
    			
    		except:
    			respond_w ="Oops! Couldn't find that address, or encountered an unknown problem. Please use the autocomplete feature and confirm that the address is located within New York City."
    			nquestions = [40.715, -74.006] * 10 #, 'Enter an address', 'in the seach field above', 'to get map results']
    			dict = []
    			dict = [[40.715, -74.006,'Enter an address in the search bar above to obtain details.', 2015, 0],[0,1,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    			map_lat = 40.83 #return_coord[0]
    			map_long = -73.99 #return_coord[1]    			
    			return render_template('nycProperty_except.html', num = nquestions, center_lat= map_lat, center_long=map_long, zoom=13, d=dict, length=1, respond=respond_w)

if __name__ == "__main__":
    app.run()
    