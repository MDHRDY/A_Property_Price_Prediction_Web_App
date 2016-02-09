from flask import Flask, render_template, request, redirect
import pandas as pd
from bokeh.embed import components 
from bokeh.plotting import figure, output_file, show
import jinja2
from IPython.display import HTML

app_tckr = Flask(__name__)

app_tckr.vars={}


template = jinja2.Template("""
<!DOCTYPE html>
<html lang="en-US">
<link rel="stylesheet" href="https://cdn.pydata.org/bokeh/release/bokeh-0.11.0.min.css" type="text/css"/>
<script type="text/javascript" src="https://cdn.pydata.org/bokeh/release/bokeh-0.11.0.min.js"></script>
<body>
    {{ script }}
    {{ div }}
    <form id='userinfoform_tckr' method='get' action='/tckr' >
    <p>
    <input type='submit' value='Go Back' />
    </p>
    </form>
</body>
</html>
""")


@app_tckr.route('/tckr', methods=['GET','POST'])
def index_tckr():
	if request.method == 'GET':   
		return render_template('userinfo_tckr.html')
	else: 
		app_tckr.vars['Ticker'] = request.form['name_tckr']
		stock_data = pd.read_csv("https://www.quandl.com/api/v3/datasets/WIKI/%s.csv?auth_token=SPdj1tC3fV-eeCdt9YGq" % app_tckr.vars['Ticker'],
        parse_dates=['Date'] )
        
    	p = figure(width=800, height=250, x_axis_type="datetime",\
    		title="%s" %app_tckr.vars['Ticker'].upper(), title_text_font_size='10pt')
    	p.line(stock_data['Date'], stock_data['Close'], color='navy', alpha=0.5)
    	p.yaxis.axis_label = "End of Day (USD)"
    	p.yaxis.axis_label_text_font_size = "9pt"
    	    	
    	script, div = components(p)
    	show(p)
    	print type(p)
    	HTML(template.render(script=script, div=div))
    	return template.render(script=script, div=div)


@app_tckr.errorhandler(500)
def pageNotFound(error):
	return render_template('error_page.html')
    
@app_tckr.errorhandler(404)
def pageNotFound(error):
	return render_template('error_page.html')


if __name__ == "__main__":
    app_tckr.run(debug=False)
    