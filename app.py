from flask import Flask, render_template, request, redirect
import pandas as pd
from bokeh.embed import components 
from bokeh.plotting import figure, output_file, show
import jinja2
from IPython.display import HTML

app = Flask(__name__)

app.vars={}


@app.route('/')
def index_tckr():  
	return render_template('userinfo_tckr.html')


@app.route('/graph', methods=['POST'])
def generate_graph():
	app.vars['Ticker'] = request.form['name_tckr']
	stock_data = pd.read_csv("https://www.quandl.com/api/v3/datasets/WIKI/%s.csv?auth_token=SPdj1tC3fV-eeCdt9YGq" \
			% app.vars['Ticker'], parse_dates=['Date'] )
			
	p = figure(width=800, height=250, x_axis_type="datetime",title="%s" \
			% app.vars['Ticker'].upper(), title_text_font_size='10pt')
	p.line(stock_data['Date'], stock_data['Close'], color='navy', alpha=0.5)
	p.yaxis.axis_label = "End of Day (USD)"
	p.yaxis.axis_label_text_font_size = "9pt"
	
	script, div = components(p)
	show(p)
	return render_template('graph.html', script=script, div=div)


@app.errorhandler(500)
def pageNotFound(error):
	return render_template('error_page.html')

  
@app.errorhandler(404)
def pageNotFound(error):
	return render_template('error_page.html')


if __name__ == "__main__":
    app.run(debug=False)
    