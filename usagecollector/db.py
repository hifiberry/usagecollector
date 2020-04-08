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

from json import dumps, loads

class DBEntry(object):
    
    def __init__(self, initial_data={}):
     
        # Do not initialize all parameters, we might not need them all
        # these will be created on demand
        if "used" in initial_data:
            self.used = float(initial_data["used"])
            
            
        if "active" in initial_data:
            self.active = initial_data["active"]
            
        if "changed" in initial_data:
            self.changed = initial_data["changed"]
        
        if "activated" in initial_data:
            self.activated = initial_data["activated"]

        if "deactivated" in initial_data:
            self.deactivated = initial_data["deactivated"]
        
    def use(self, counter):
        if counter > 0:
            try:
                self.used = self.used + counter
            except:
                self.used = counter

        
    def activate(self, active = True):
        try:
            if self.active != active:
                self.active = active
                self.changed += 1
        except:
            self.active = active
            self.changed = 1
        
        if active:
            try:
                self.activated = self.activated + 1
            except:
                self.activated = 1
        else:
            try:
                self.deactivated = self.deactivated + 1
            except:
                self.deactivated = 1
                
    def get(self, attribute, default_value=0):
        return self.__dict__.get(attribute, default_value)
            
        
class StatsDB(object):

    def __init__(self):
        
        self.mem_db = {}
        
    def db(self):
        return self.mem_db
    
    def get(self, key, create = True):
        if key in self.mem_db:
            return self.mem_db[key]
        elif create:
            record = DBEntry()
            self.mem_db[key]=record
            return record
        else:
            return None
        
    def keys(self):
        return self.mem_db.keys()
    
    def clear(self):
        self.mem_db.clear()
        
    def __len__(self):
        return len(self.mem_db)
    
    def asJson(self):
        # convert objects to dicts first
        json_dict = {}
        for key in self.mem_db.keys():
            json_dict[key]=self.mem_db.get(key).__dict__
            
        return dumps(json_dict)
            
    def fromJson(self, json_str):
        memdb={}
        
        stats = loads(json_str)
        for key in stats:
            data = stats[key]
            dbe = DBEntry(data)
            memdb[key] = dbe
        
        self.mem_db = memdb
        
    def writeFile(self,filename):
        with open(filename, "w") as datafile:  
            datafile.write(self.asJson())
        
    def readFile(self, filename):
        with open(filename, "r") as datafile:
            json_str = datafile.read()
            self.fromJson(json_str)
