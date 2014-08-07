# -*- coding: utf-8 -*-
# @author: wenwu

from flask import Flask, render_template
app = Flask('yunhetong')

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/test/<path:filename>')
def template_load(filename=None):
    if not filename:
        return render_template('index.html')
    else:
        return render_template(filename+'.html')