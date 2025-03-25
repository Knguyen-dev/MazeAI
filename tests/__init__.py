

'''
Gets the current working directory and adds src onto it.
'''
import os
import sys

cwd = os.getcwd()
sys.path.insert(0, os.path.join(cwd, "src"))