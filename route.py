#!/usr/bin/env python
import os
from flask import Flask, redirect, render_template

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/hello/')
def hello():
    #return "hello_world"
    return redirect("http://silapha.com:8080/geoserver/wms", code=302)

if __name__ == '__main__':
    app.run(debug=True)
#    port = int(os.environ.get('PORT', 5000))
#    app.run(host='0.0.0.0', port=port)
