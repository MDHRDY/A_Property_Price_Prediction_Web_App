from flask import Flask,render_template, request, redirect
#import dill


#with open("X.dill", "r") as f:
#    X1 = dill.load(f)    
#with open("SGD_regress.dill", "r") as f:
#    sgd = dill.load(f)


app_lulu = Flask(__name__, static_url_path = "", static_folder = "")


app_lulu.vars={}

@app_lulu.route('/nycProperty.html',methods=['GET','POST'])
@app_lulu.route('/',methods=['GET','POST'])
def index_lulu():
    nquestions=''
    if request.method == 'GET':
    # 'user_info_heat_tut2.html'
    	return render_template('nycProperty.html', num = nquestions) #'leaflet_w_d3_external_data_ex_nyc.html', num=nquestions)
    else:
    	#request was a POST
    	app_lulu.vars['name'] = request.form['name_lulu']
    	#app_lulu.vars['age'] = request.form['age_lulu']
    	
    	nquestions = app_lulu.vars['name']
    	#if nquestions == 'yes':
    	#	nquestions = sgd.transform(X1)
    	return render_template('nycProperty.html', num = nquestions)

    			
if __name__ == '__main__':
    app_lulu.run(debug=False)
