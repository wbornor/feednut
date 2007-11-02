import unittest

from properties import Properties

class PropertiesTestCase(unittest.TestCase):
    def setup(self):
        pass
    def teardown(self):
        pass
    def runTest(self):
        """Test blank"""
        prefString= ""
        prefs = Properties(prefString)
        prefString = "default.name=Bilbo Baggins\nhomepage.feeds=42,24"
        prefs = Properties(prefString)
        assert cmp('Bilbo Baggins', prefs.get('default.name')) == 0, 'Error retrieving value from key'
        assert cmp('', prefs.get('jeff')) == 0, "Missing keys should default to blank string"
        prefs.set('Hulk', 'Hogan')
        assert cmp('Hogan', prefs.get('Hulk')) == 0, 'Error retrieving set key/value'
        stringValue = prefs.convertToPropertiesFile()
        #this last test needs to be fixed, can fail if keys are not brought back in same order
        assert cmp(prefString + "\nHulk=Hogan", stringValue) == 0, 'Error converting to properties'
        prefString = "jeff=1"
        prefs = Properties(prefString)
        assert cmp('1', prefs.get('jeff')) == 0
        assert cmp('1', prefs.pop('jeff')) == 0
        try:
            prefs.pop('badkey')
            unittest.fail('A KeyError exception should have prevented this')
        except KeyError:
            pass
        assert False  == prefs.has_key('jeff')
t = PropertiesTestCase()
t.runTest()
