'''
Created on 26.02.2020

@author: matuschd
'''
import unittest

from stats.client import StatsClient
from stats.server import StatsWebserver

class TestClientServer(unittest.TestCase):

    def testClientServer(self):
        
        server = StatsWebserver("127.0.0.1",31415)
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
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()