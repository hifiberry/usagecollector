'''
Created on 26.02.2020

@author: matuschd
'''
import unittest
import tempfile
import os

from usagecollector.client import StatsClient
from usagecollector.server import StatsWebserver

class TestClientServer(unittest.TestCase):

    def testClientServer(self):
        
        filename = tempfile.gettempdir()+"/89216789236faadssdawq12216789216789.json"
        
        server = StatsWebserver("127.0.0.1",31415, 
                                load_data=False, 
                                dbfile = filename)
        client = StatsClient("127.0.0.1",31415)
        
        server.start()
        
        client.activate("test1")
        client.activate("test2")
        
        record = client.get_data("test1")
        self.assertEqual(record.get("active"),1)
        self.assertEqual(record.get("changed"),1)
        
        record = client.get_data("test2")
        self.assertEqual(record.get("active"),1)
        self.assertEqual(record.get("changed"),1)
        
        # this record does not exist
        record = client.get_data("test3")
        self.assertEqual(record.get("active"),0)
        self.assertEqual(record.get("changed"),0)
        
        # Check keys, it should be test1-test3
        keys = client.keys()
        self.assertEqual(len(keys),3)
        self.assertSetEqual(set(keys), set(["test1","test2","test3"]))
        
        # test store/clear/restore
        client.store()
        client.clear()
        keys = client.keys()
        self.assertEqual(len(keys), 0)
        
        self.assertTrue(os.path.isfile(filename))
        
        client.restore()
        keys = client.keys()
        self.assertSetEqual(set(keys), set(["test1","test2","test3"]))
        
        # test JSON export
        client.clear()
        empty = client.dump()
        self.assertEqual({}, empty)
        client.restore()
        db = client.dump()
        print(db)
        self.assertTrue("test1" in db)
        self.assertTrue("test2" in db)
        self.assertTrue("test3" in db)
    

        
        os.remove(filename)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()