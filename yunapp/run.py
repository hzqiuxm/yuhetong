# -*- coding: utf-8 -*-
# @author: wenwu

from yunapp import app
app.debug = True
#app.run(host='0.0.0.0', port=5005)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5055)
