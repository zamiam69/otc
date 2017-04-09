import os

import requests
import jinja2

class RequestManager(object):
    _template_path = ['templates']

    """Factory Pattern based on
https://krzysztofzuraw.com/blog/2016/factory-pattern-python.html"""

    def __init__(self, *args, **kwargs):
        self._templatePath = os.path.join()
        loader = jinja2.FileSystemLoader(os.path.join(_template_path))
        j2env = jinja2.Environment(loader=FileSystemLoader)
        pass


class Request(object):
    def __init__(self, *args, **kwargs):
        pass

    def generate(self):
        raise NotImplementedError()

class POSTRequest(Request):
    def generate(self):
        pass
    

# vim: sts=4 sw=4 ts=4 et:
