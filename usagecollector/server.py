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

'''
Copyright (c) 2019 Modul 9/HiFiBerry

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

import logging
import threading
import json
import os 
import sys

from bottle import Bottle, response

from usagecollector.db import StatsDB

class StatsWebserver():

    def __init__(self,
                 host='0.0.0.0',
                 port=3141,
                 dbfile="/var/lib/hifiberry/usage.json",
                 load_data=True):
        super().__init__()
        self.port = port
        self.host = host
        self.bottle = Bottle()
        self.route()
        self.db = StatsDB()
        self.dbfile = dbfile
        
        if load_data and os.path.isfile(dbfile):
            try:
                self.db.readFile(dbfile)
            except Exception as e:
                logging.error("can't read %s (%s)",
                              dbfile, e)
        
    def route(self):
        self.bottle.route('/api/activate/<key>',
                          method="POST",
                          callback=self.activate_handler)
        self.bottle.route('/api/deactivate/<key>',
                          method="POST",
                          callback=self.deactivate_handler)
        self.bottle.route('/api/use/<key>/<duration>',
                          method="POST",
                          callback=self.usage_handler)
        self.bottle.route('/api/record/<key>',
                          method="GET",
                          callback=self.record_handler)
        self.bottle.route('/api/clear',
                          method="POST",
                          callback=self.clear_handler)
        self.bottle.route('/api/store',
                          method="POST",
                          callback=self.store_handler)
        self.bottle.route('/api/restore',
                          method="POST",
                          callback=self.restore_handler)
        self.bottle.route('/api/keys',
                          method="GET",
                          callback=self.keys_handler)
        self.bottle.route('/api/dump',
                          method="GET",
                          callback=self.dump_handler)

    def startServer(self):
        self.bottle.run(port=self.port,
                        host=self.host)

    def activate_handler(self, key, activate = True):
        record = self.db.get(key, create=True)
        record.activate(activate)
        return "ok"

    def deactivate_handler(self, key):
        return self.activate_handler(key, activate=False)

    def usage_handler(self, key, duration):
        record = self.db.get(key, create=True)
        duration = int(duration)
        record.use(duration)
        return "ok"

    def record_handler(self,key):
        record = self.db.get(key, create=True)
        response.headers['Content-Type'] = 'application/json'
        data = json.dumps(record.__dict__)
        return data
    
    def keys_handler(self):
        keys = list(self.db.keys())
        response.headers['Content-Type'] = 'application/json'
        data = json.dumps(keys)
        return data
    
    def clear_handler(self):
        self.db.clear()
        return "ok"
    
    def store_handler(self):
        self.db.writeFile(self.dbfile)
        return "ok"
  
    def restore_handler(self):
        self.db.readFile(self.dbfile)
        return "ok"
    
    def dump_handler(self):
        self.db.writeFile(self.dbfile)
        response.headers['Content-Type'] = 'application/json'
        json_str = self.db.asJson()
        return json_str
    
    # ##
    # ## end URL handlers
    # ##

    # ##
    # ##  thread methods
    # ##

    def start(self, daemon = True):
        self.thread = threading.Thread(target=self.startServer, args=())
        self.thread.daemon = True
        self.thread.start()
        logging.info("started web server on port {}".format(self.port))

    def is_alive(self):
        if self.thread is None:
            return True
        else:
            return self.thread.is_alive()

    # ##
    # ## end thread methods
    # ##

    def __str__(self):
        return "statsserver@{}".format(self.port)


if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        if "-v" in sys.argv:
            logging.basicConfig(format='%(levelname)s: %(module)s - %(message)s',
                                level=logging.DEBUG)
            logging.debug("enabled verbose logging")
    else:
        logging.basicConfig(format='%(levelname)s: %(module)s - %(message)s',
                            level=logging.DEBUG)

    statsServer=StatsWebserver(
        host='0.0.0.0',
        port=3141,
        debug=False,
        dbfile="/var/lib/hifiberry/usage.json",
        load_data=True)
    
    statsServer.start(daemon=False)
