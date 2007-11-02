from UserDict import DictMixin

class Properties(DictMixin):
    """ Takes a java like properties file seperated by new lines and stores it as a dictionary object"""
    def __init__(self, prefString):
        self.prefString = prefString
        self.data = {}
        self.data =  self.parse()
        self.properties = ""
    def parse(self):
        dict = {}
        string = self.prefString.strip()
        if len(string) == 0: return dict
        keyvalues = string.split('\n')
        for keyvalue in keyvalues:
            split = keyvalue.split('=')
            assert len(split) == 2
            key = split[0].strip()
            value = split[1].strip()
            dict[key] = value
        return dict
    
    def __getitem__(self, key):
        return self.data[key]
    def get(self,key, default = ""):
        if self.data.has_key(key) is False: return default
        return self.data[key]
    def set(self,key,value):
        self.data[key] = value
        #reset the properties value
        self.properties = ""
    def pop(self, key):
        if self.data.has_key(key) == False:
            raise KeyError
        return self.data.pop(key)
    def has_key(self,key):
        return self.data.has_key(key)
    def keys(self):
        return self.data.keys()
    def convertToPropertiesFile(self):
        """ Takes the key values and converts them to a java like properties file seperated by new line characters"""
        if len(self.properties) > 0: 
            return self.properties
        value = ""
        split = ""
        for key in self.data.keys():
            value = value + split + key + "=" + self.data[key]
            split = "\n"
        self.properties = value
        return self.properties