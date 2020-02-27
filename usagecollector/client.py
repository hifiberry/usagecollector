'''
Copyright (c) 2020 Modul 9/HiFiBerry

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import requests
import logging

my_client = None

def client():
    global my_client
    if my_client is None:
        my_client = StatsClient()
    return my_client
        
def report_activate(key):
    try:
        return client().api_post(["activate",key])
    except: 
        return False

def report_deactivate(self, key):
    try:
        return client().api_post(["deactivate",key])
    except:
        return False

def report_usage(self, key, duration):
    try:
        return client().api_post(["use",key,duration])
    except:
        return False


class StatsClient():
    
    def __init__(self, host="127.0.0.1", port=3141):
        self.host = host
        self.port = port
        self.baseUrl = "http://"+self.host+":"+str(self.port)+"/api/"

    def activate(self, key):
        return self.api_post(["activate",key])
    
    def deactivate(self, key):
        return self.api_post(["deactivate",key])
    
    def usage(self, key, duration):
        return self.api_post(["use",key,duration])
    
    def clear(self):
        return self.api_post(["clear"])

    def store(self):
        return self.api_post(["store"])

    def restore(self):
        return self.api_post(["restore"])
    
    def get_data(self, key):
        data = self.api_get(["record",key])
        return data
    
    def keys(self):
        data = self.api_get(["keys"])
        return data
    
    def dump(self):
        data = self.api_get(["dump"])
        return data
    
    def url(self, args):
        return self.baseUrl + "/".join(args)

    def api_post(self, args, data=None):
        return requests.post(self.url(args), data=data)

    def api_get(self, args):
        response = requests.get(self.url(args))
        try:
            return response.json()
        except Exception as e:
            logging.error("unexpected response")
            logging.exception(e)