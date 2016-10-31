loggr : temp log sharing
=========================

A simple Python logging handler which transmits logs to a centralized service
(also provided) with minimal work from both the web server side and the Python
side as well. For help, install the package, run loggr.py, and visit
localhost:8888 for more information.

In the most basic form, simply add another handler to your existing logging
class via::

    import logging
    from loggr import LoggrHandler

    handler = LoggrHandler(url='http://someurl/', logname='optional-name')
    logger = logging.getLogger('root')
    logger.addHandler(handler)
