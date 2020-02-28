'''
Created on 26.02.2020

@author: matuschd
'''
import unittest
import tempfile

from usagecollector.db import DBEntry, StatsDB

class DBEntryTest(unittest.TestCase):


    def testDBEntryCreate(self):
        entry = DBEntry()
        self.assertEqual(entry.get("active"), False)
        self.assertEqual(entry.get("used"), 0)
        self.assertEqual(entry.get("changed"), 0)

        entry = DBEntry({"active": 1, "used":"17", "changed": 3})
        
        self.assertEqual(entry.get("active"), True)
        self.assertEqual(entry.get("used"), 17)
        self.assertEqual(entry.get("changed"), 3)
        

    def testDBEntryActivate(self):
        entry = DBEntry()
        self.assertEqual(entry.get("active"), False)
        self.assertEqual(entry.get("changed"), 0)
        entry.activate()
        self.assertEqual(entry.get("active"), True)
        self.assertEqual(entry.get("changed"), 1)
        entry.activate(False)
        self.assertEqual(entry.get("active"), False)
        self.assertEqual(entry.get("changed"), 2)
        entry.activate(False)
        self.assertEqual(entry.get("active"), False)
        self.assertEqual(entry.get("changed"), 2)
        self.assertEqual(entry.get("activated"), 1)
        self.assertEqual(entry.get("deactivated"), 2)
        
    def testDBEntryUse(self):
        entry = DBEntry()
        self.assertEqual(entry.get("used"), 0)
        self.assertEqual(entry.get("changed"), 0)
        entry.use(1)
        self.assertEqual(entry.get("used"), 1)
        self.assertEqual(entry.get("changed"), 0)
        entry.use(1)
        self.assertEqual(entry.get("used"), 2)
        entry.use(10)
        self.assertEqual(entry.get("used"), 12)
        entry.use(-1)
        self.assertEqual(entry.get("used"), 12)
        entry.use(0.1)
        self.assertEqual(entry.get("used"), 12.1)
        
class StatsDBTest(unittest.TestCase):
    
    def create_test_data(self):
        db = StatsDB()
        db.get("test1").use(1)
        db.get("test2").use(2)
        db.get("test3").use(3)
        return db
        
    
    def testDBRecords(self):
        db = StatsDB()
        self.assertIsNotNone(db.get("test1"))
        self.assertIsNotNone(db.get("test2"))
        self.assertIsNone(db.get("test3",create=False))
        self.assertEqual(len(db), 2)
        
    def testDump(self):
        db1 = self.create_test_data()
        
        json = db1.asJson()
        
        db2 = StatsDB()
        db2.fromJson(json)
        
        self.assertEqual(len(db2), len(db1))
        self.assertSetEqual(set(db1.keys()), set(db2.keys()))
        self.assertEqual(db2.get("test3").used, 3)
        
    def testFileBackup(self):
        db1 = self.create_test_data()
        filename = tempfile.gettempdir()+"/8921678923678216782178167818186712216789216789.json"
        
        db1.writeFile(filename)
        
        db2 = StatsDB()
        self.assertEqual(len(db2), 0)
        self.assertEqual(db2.get("test3").get("used"), 0)
        
        db2.readFile(filename)
        
        self.assertEqual(len(db2), len(db1))
        self.assertSetEqual(set(db1.keys()), set(db2.keys()))
        self.assertEqual(db2.get("test3").used, 3)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()