from flask import Flask, render_template, request, redirect
import pandas as pd, numpy as np
import urllib
import simplejson as json
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.resources import INLINE


app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/graph')
def graph():
    tname = request.args.get('tname','GOOG')
    ttypes = {'cprice':0,'acprice':0,'oprice':0,'aoprice':0}
    for t in ttypes:
        if request.args.get(t,0):
            ttypes[t] = 1
            ttype = t
    print (sum(ttypes.values()))
    if sum(ttypes.values()) != 1:
        return 'Please check one of the options' 
    if ttype in ['cprice','oprice']:
        hres = urllib.request.urlopen('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='\
                       +tname+'&apikey=817F9YH6KXOZQ2QU')
    else:
        hres = urllib.request.urlopen('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol='\
                       +tname+'&apikey=817F9YH6KXOZQ2QU')
    data = json.loads(hres.read().decode("utf-8"))
    if 'Error Message' in data:
        return ('Please check your ticker symbol')
    else:
        a = pd.DataFrame(data['Time Series (Daily)']).T.iloc[:,:4]
    a.columns = ['open','high','low','close']
    if ttype == 'aprice' or ttype=='cprice':
        x = np.array(a['close'].index,dtype=np.datetime64)[:30]
        y = np.array(a['close'].values,dtype='f')[:30]
    else:
        x = np.array(a['open'].index,dtype=np.datetime64)[:30]
        y = np.array(a['open'].values,dtype='f')[:30]
    # start frawing figure 
    p = figure(title='Quandl WIKI EOD Stock Prices - 2020', x_axis_label= 'x', y_axis_label='y',x_axis_type="datetime")
    p.line(x,y,legend_label = tname, line_width = 2)
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'
    #show(p)
    
    # grab the static resources
    script, div = components(p)
    kwargs = {'script': script, 'div': div}
    kwargs['title'] = 'bokeh-with-flask'    
    filename = 'https://www.google.com/search?tbm=fin&q='+tname
    return render_template('showresult.html', filename=filename,**kwargs)   
    
if __name__ == '__main__':
    app.run(debug=True)
