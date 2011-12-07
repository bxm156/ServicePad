'''
Created on Dec 3, 2011


@author: Bryan
'''
import sys
import os

PROJECT_ROOT = "/Users/Bryan/DjangoWorkspace/ServicePad/ServicePad"
SITE_ROOT = os.path.dirname(PROJECT_ROOT)

sys.path.append(SITE_ROOT)
sys.path.append(PROJECT_ROOT + '/apps')
sys.path.append(PROJECT_ROOT + '/libs')