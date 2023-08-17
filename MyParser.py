'''
Created on Sep 26, 2013

@author: priyank
'''
import argparse
import sys

class MyParser(argparse.ArgumentParser):
    '''
    classdocs
    '''
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)
        