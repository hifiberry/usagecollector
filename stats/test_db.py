'''
Created on 26.02.2020

@author: matuschd
'''
import unittest

from stats.db import DBEntry, StatsDB

class DBEntryTest(unittest.TestCase):


    def testDBEntryCreate(self):
        entry = DBEntry()
        self.assertEqual(entry.active, False)
        self.assertEqual(entry.used, 0)
        self.assertEqual(entry.changed, 0)

        entry = DBEntry({"active": 1, "used":"17", "changed": 3})
        
        self.assertEqual(entry.active, True)
        self.assertEqual(entry.used, 17)
        self.assertEqual(entry.changed, 3)
        

    def testDBEntryActivate(self):
        entry = DBEntry()
        self.assertEqual(entry.active, False)
        self.assertEqual(entry.changed, 0)
        entry.activate()
        self.assertEqual(entry.active, True)
        self.assertEqual(entry.changed, 1)
        entry.activate(False)
        self.assertEqual(entry.active, False)
        self.assertEqual(entry.changed, 2)
        entry.activate(False)
        self.assertEqual(entry.active, False)
        self.assertEqual(entry.changed, 2)
        
    def testDBEntryUse(self):
        entry = DBEntry()
        self.assertEqual(entry.used, 0)
        self.assertEqual(entry.changed, 0)
        entry.use(1)
        self.assertEqual(entry.used, 1)
        self.assertEqual(entry.changed, 0)
        entry.use(1)
        self.assertEqual(entry.used, 2)
        entry.use(10)
        self.assertEqual(entry.used, 12)
        entry.use(-1)
        self.assertEqual(entry.used, 12)
        entry.use(0.1)
        self.assertEqual(entry.used, 12.1)
        
class StatsDBTest(unittest.TestCase):
    
    def testDBRecords(self):
        db = StatsDB()
        self.assertIsNotNone(db.get("test1"))
        self.assertIsNotNone(db.get("test2"))
        self.assertIsNone(db.get("test3",create=False))
        self.assertEqual(len(db), 2)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()