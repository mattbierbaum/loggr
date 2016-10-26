import atexit
import logging
import requests

_active_logs = {}

def get_logurl(url, num):
    return '{}/{:03d}'.format(url, num)

def get_number(url):
    return int(requests.put('{}'.format(url)).text)

class LoggrHandler(logging.StreamHandler):
    def __init__(self, url, num=None, logname=''):
        """ A very simple web logging interface using loggr website """
        self.url = url
        self.logname = logname
        self.num = num or get_number(self.url)
        _active_logs[self.num] = self.url
        super(LoggrHandler, self).__init__()

    def emit(self, record):
        """ Send the message to the website """
        q = requests.post(get_logurl(self.url, self.num), {
            'name': self.logname, 'log': self.format(record)+'\n'
        })
        if q.status_code != 200:
            raise requests.exceptions.HTTPError('loggr server could not be reached')

    def __del__(self):
        super(LoggrHandler, self).__del__()

@atexit.register
def delete_all():
    for k,v in _active_logs.iteritems():
        requests.delete(get_logurl(v, k))


