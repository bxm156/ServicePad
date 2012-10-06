'''
Created on Dec 3, 2011

Local path settings. Do not commit this file if you can help it.
You can modify your environmental variables to change these settings

@author: Bryan
'''
import sys
import os

#Modify these to set defaults for your local development
PROJECT_ROOT = "/Users/Bryan/DjangoWorkspace/ServicePad"
APP_DIR = "ServicePad"

#In Production, we will use environmental variables to overide any local settings

#If you can, use the environmental variables in your local development.
# PROJECT_ROOT
# APP_DIR

PROJECT_ROOT = os.getenv("PROJECT_ROOT", PROJECT_ROOT)
APP_DIR = os.getenv("APP_DIR",APP_DIR)
APP_ROOT = os.path.join(PROJECT_ROOT,APP_DIR)

#For handling the database
# DATABASE_URL - https://github.com/kennethreitz/dj-database-url
DATABASE_URL = 'sqlite:////' + PROJECT_ROOT + '/db/sqlite.db'

#Add the proper directories to our path
sys.path.append(PROJECT_ROOT)
sys.path.append(os.path.join(APP_ROOT,'apps'))
sys.path.append(os.path.join(APP_ROOT,'libs'))
