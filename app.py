# -*- coding: utf-8 -*-
#!/yunhetong/
__author__ = 'Seanwu'

from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def hello_world():
#   你看不见我   你看不见我~~~
    return 'Hello World!'


@app.route('/test/<path:filename>')
def template_load(filename=None):
    if not filename:
        return render_template('index.html')
    else:
        return render_template(filename+'.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
