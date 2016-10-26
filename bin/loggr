#!/usr/bin/env python
import os
import json
import base64
import string
import random

import tornado
import tornado.web
import tornado.ioloop
import tornado.options

tornado.options.options.define("port", default=8888)
tornado.options.options.define("addr", default="127.0.0.1", help="port to listen on")

FAVICON =  "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgAgMAAAAOFJJnAAAABGdBTUEAALGPC/xhBQAAAAFzUkdCAK7OHOkAAAAMUExURRwcHAAAAAAAAPX19bKWAtEAAAACdFJOU7cBqhDF0QAAAGJJREFUGNNjCHVgAALGUIaQVWAgyhAEYbQyeEEYCxmyIIyVDFoQxgriGIu1oIzVp2BSn2CMPTDGei0oY/UrdJE96Lrg5izWWsDAoAW2q////1MrSHMY3DtwD8K9DA8EWLAAAPg1j+sXiGe2AAAAAElFTkSuQmCC"

INDEX_CONTENT = string.Template(
"""<link id="favicon" rel="shortcut icon" type="image/png"  href="data:image/png;base64,$favicon">

<html><head><title>loggr : log share</title></head>
<body style='background: #ffffff;background-size: 100% auto;'>
<center><pre style='font-size:48px;margin:10px;'>LOGGR : LOG SHARING</pre></center>
<pre style='width:640px;margin:auto;background-color:rgba(155,155,155,0.5);padding:10px;'>
$content</pre></center></body></html>""")

LIST_STRING = string.Template(
"""<a href=/$num style='text-decoration: none; color: #0944a3;'>$num ($name)</a>: $summary""")

HELP_STRING = \
"""
Loggr is a simple utility to connect Python's logging module to an external
website for easy viewing. In order to use, you must first install loggr by:

    pip install loggr

Then, you must start the website:

    loggr --port=PORT

and then add the logging handler to your project. All logs will automatically
be transmitted to the loggr service:

    from loggr import LoggrHandler
    handler = LoggrHandler(url='http://someurl/', logname='optional-name')

Add this handler to your logging

    import logging
    logger = logging.getLogger('root')
    logger.addHandler(handler)
"""

data = {}

def escape_html(text):
    return text.replace('<', '&lt;').replace('>', '&gt;')

#=============================================================================
# The actual web application now
#=============================================================================
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/+$", MainHandler),
            (r"/+([0-9]{3})$", LogHandler)
        ]
        super(Application, self).__init__(handlers, gzip=True)

class MainHandler(tornado.web.RequestHandler):
    def error(self, text):
        self.clear()
        self.set_status(404)
        self.write(text)
        self.finish()

    def page_home(self):
        def _summary(i):
            num = '%03d' % i
            name = data[i]['name']
            tail = data[i]['log']

            tail = tail[tail.rfind('\n', 0, len(tail)-1):].strip('\n')
            tail = tail[:50] + '...'
            tail = escape_html(tail)
            return LIST_STRING.substitute(
                num=num, name=name, summary=tail
            )

        lognums = sorted(data.keys())
        loglist = '\n'.join([
            _summary(n) for n in lognums
        ])
        content = """
            <center><h1>Active logs</h1></center>{}<br/>
            <center><h1>Howto</h1></center>{}
        """.format(loglist, HELP_STRING)

        self.write(INDEX_CONTENT.substitute(
            favicon=FAVICON, content=content
        ))
        self.finish()

    def page_new(self):
        nextlog = min(list(
            set(range(1000)).difference(set(data.keys()))
        ))
        self.write(str(nextlog))
        self.finish()

    def get(self):
        self.page_home()

    def put(self):
        self.page_new()

class LogHandler(tornado.web.RequestHandler):
    def error(self, text):
        self.clear()
        self.set_status(404)
        self.write(text)
        self.finish()

    def get(self, args):
        n = int(args)
        title = '<center><h1>{}</h1></center>\n'.format(data[n]['name'])
        self.write(INDEX_CONTENT.substitute(
            favicon=FAVICON, content=title+escape_html(data[n]['log'])
        ))
        self.finish()

    def post(self, args):
        num = int(args)
        name = self.request.arguments.get('name')
        line = self.request.arguments.get('log')

        if not num in data:
            data[num] = {'name': '', 'log': '\n'}

        data[num]['name'] = name[0]
        data[num]['log'] = data[num]['log'] + line[0]

    def delete(self, args):
        num = int(args)
        if num in data:
            data.pop(num)
        else:
            self.error('Log index not found')

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = Application()
    app.listen(tornado.options.options.port, tornado.options.options.addr)
    tornado.ioloop.IOLoop.instance().start()

