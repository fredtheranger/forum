
import os, sys
import ConfigParser
import __main__

class Config:
    
    def __init__(self):
       
        # In an attempt to be sneaky here, we'll use the forum.ini from
        # the test directory unless we are being called from the main forums.py.
        # This is an easier way to allow config to work for both the main
        # app and the unittests (even though they are not true unit tests)
        # since we'd have to import an external library to mock objects properly 
        spath = os.path.dirname(__main__.__file__).split('/')[-1] 
        if spath == '':
            spath = sys.path[0].split('/')[-1]
             
        if spath == 'forum':
            basedir = os.path.dirname(__main__.__file__)
            configfile = os.path.join(basedir, 'forum.ini')
        else:
            configfile = os.path.join(os.path.dirname(__file__), '..', '..', 'test', 'test.ini')
        
        if not os.path.exists(configfile):
            raise OSError(2, 'No such file or directory', configfile)
        
        #print 'Reading configuration from %s' % configfile
        
        self.config = ConfigParser.ConfigParser()
        self.config.read(configfile)
        
    def get(self, param):
        section, option = param.split('.')
        return self.config.get(section, option)
        