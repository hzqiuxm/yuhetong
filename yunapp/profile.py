# -*- coding: utf-8 -*-
# @author: wenwu

from werkzeug.contrib.profiler import ProfilerMiddleware
from yunapp import app

app.config['PROFILE'] = True
app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions = [30])
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1090, debug=True)
