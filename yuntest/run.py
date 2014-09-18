# -*- coding: utf-8 -*-
# @author: seanwu

from flask import Flask

app = Flask(__name__)
app.debug = True

if __name__ == '__main__':
    print 'aaaa'
    app.run(host='0.0.0.0', port=5060)

#
# @app.route("/test/contract")
# def contract_test():
#     return render_template('covhtml/index.html')


@app.route('/')
def hello_world():
    print 'bbb'
    return 'Hello World'


# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('covhtml/index.html'), 404