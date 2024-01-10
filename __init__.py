# import libraries
import pandas as pd
import numpy as np

import json

import datetime as dt
from datetime import datetime
import time as tm

import os
import fnmatch
import random
import string


import plotly.express as px
from dash import Dash, html, dcc

import warnings
warnings.filterwarnings('ignore')

# import functions
path_data_sources = os.path.dirname(os.path.abspath(__file__))
exec(open(path_data_sources +'/lib/functions').read())


class Core():
    '''
    It's an abstract class
    '''


    def __new__(cls, *args, **kwargs):
        ''' Construct new object '''
        return super().__new__(cls)


    def __init__(self, path='.', name='', description='Default description'):
        ''' Set up defaults attributes '''

        # Main attributes (single variables)
        self.path = path
        self.name = name
        self.description = description
        self.index = 'index.json'

        self.inners = self.get_inners()


    def get_inners(self):
        pass
        return {}


    def __del__(self):
        del self.path, self.name, self.description, self.index

    # Aggregate main attributes

    def path_name(self):
        ''' Construct a full path  '''
        return str(self.path) + str(self.name) + '/'


    def path_name_index(self):
        ''' Construct a full path to index-file '''
        return self.path_name() + self.index


    def header(self):
        ''' Construct info '''
        header = dict(
                 zip(
                 ['Name',
                  'Description',
                  'Path to index-file'],
                 [self.name,
                  self.description,
                  self.path_name_index()]))
        return header


    def __repr__(self):
        ''' Construct info to print '''
        return 'Name: ' + str(self.name) + '\n'\
               'Description: ' + str(self.description) + '\n'\
               'Path to index-file: ' + self.path_name_index() + '\n'


    def info(self):
        ''' Output abstract information about data sources '''
        print(self)
        print('Attributes:', self.main_attributes())


    def main_attributes(self):
        ''' Construct dictionary of main attributes '''
        return dict(zip(['path', 'name', 'description', 'index'],
                        [self.path, self.name, self.description, self.index]))


    def main_dictionary(self):
        ''' Construct object as dictionary '''
        header = self.header()
        attributes = self.main_attributes()
        dictionary = dict(zip(['Header', 'Attributes'],
                              [header, attributes]))
        return dictionary


    # Methods, that change main attributes

    def set_new_path(self):
        ''' Set a new path '''
        self.path = input('Set path: ')


    def set_new_name(self):
        ''' Set a new name '''
        self.name = input('Set name: ')


    def set_new_description(self):
        ''' Set a new description '''
        self.description = input('Input a new description: ')


    def set_attributes(self,
                       path=True,
                       name=True,
                       description=True):
        ''' Set a new group parametres '''
        if path: self.set_new_path()
        if name: self.set_new_name()
        if description: self.set_new_description()

    # Physical operations with object (open, save, remove, rename and other)

    def save(self):
        ''' Save data to hard drive '''
        makedir(self.path_name())
        with open(self.path_name_index(), 'w') as file:
            json.dump(self.main_dictionary(), file, ensure_ascii=False, indent=4)

    def close():
        ''' Remove object '''
        pass


    def save_as(self):
        ''' Save a new copy of data (rename and save it) '''
        self.set_attributes()
        self.save()


    def open(self, path, name):
        '''
        Open existing index-file and upload data to buffer
        Set a change-counter in zero
        '''
        path_name = path + name + '/'
        if 'index.json' in os.listdir(path_name):
            with open(path_name + 'index.json', 'r') as index_json:
                index_json = json.load(index_json)

            # Load attributes
            attributes = index_json.get('Attributes')
            self.path = attributes.get('path')
            self.name = attributes.get('name')
            self.description = attributes.get('description')
            self.index = attributes.get('index')
        else:
            print('File "index.json" not exist')


class Sources(Core):
    '''
    It's a main singleton class
    '''

    # Singleton pattern
    __instance = None
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance


    def __init__(self, path='.', name='', description='Default description'):
        ''' Set up defaults attributes '''
        super().__init__(path, name, description)

"""
class Source(Core):
    '''
    This class working with a particular data source
    Source contains "indicators" and their history
    Every source have got a "key": one or more "indicators"
    It used as primary key for updating data source
    '''

    def __new__(cls, *args, **kwargs):
        ''' Construct new object '''
        return super().__new__(cls)

    def __init__(self, path='.', name='', description='Default description'):
        ''' Set up defaults attributes of source'''

        super().__init__(path, name, description)

        # Key (unique indicator or combination of indicators)
        self.key = []


        # Working directories
        self.source_directories()

        # Data source
        self.indicators = dict(zip(
            ['indicator_1', 'indicator_2', 'indicator_3'],
            ['path_to_1/','path_to_2/','path_to_3/']
            ))

        # log changes to buffer array:
        self.changes = []


    def source_path(self):
        ''' Construct a full path to source index-file '''
        return self.path + '/' + self.name + '/'

    def source_directories(self):
        ''' Construct paths to working directories of data source '''
        # main dir
        source_path = self.source_path()
        # all loaded data of source
        self.load = source_path + 'load/'
        # path for searching updates
        self.upload = source_path + 'upload/'
        self.upload_tmp = source_path + 'upload/tmp/'
        # archive
        self.archive = source_path + 'archive/'
        return self.load, self.upload, self.upload_tmp, self.archive

    def index_path(self):
        ''' Construct a full path to source index-file '''
        return self.source_path() + self.index


    def header(self):
        ''' Construct info '''
        return 'Name of source: ' + self.name + '\n'\
               'Description: ' + self.description + '\n'\
               'Path to index-file: ' + self.index_path() + '\n'


    def attributes(self):
        ''' Construct list of main attributes '''
        return dict(zip(['path', 'name', 'description', 'index', 'key'],
               [self.path, self.name, self.description, self.index, self.key]))


    def set_new_path(self):
        ''' Set a new pathname to source '''
        change = ['Change path', self.path]
        self.path = input('Set path: ')
        # Change working directories
        self.source_directories()
        change.append(self.path)
        self.changes.append(change)


    def set_new_name(self):
        ''' Set a source name '''
        change = ['Change name', self.name]
        self.name = input('Set name: ')
        # Change working directories
        self.source_directories()
        change.append(self.name)
        self.changes.append(change)


    def set_new_description(self):
        ''' Set a more abroad descripption of source '''
        change = ['Change description', self.description]
        self.description = input('Input description of sources: ')
        change.append(self.description)
        self.changes.append(change)


    def set_new_key(self):
        ''' Set a source key (or keys) '''
        change = ['Change key', self.key]
        new_key = input('Set key: ')
        self.key.append(new_key)
        change.append(self.key)
        self.changes.append(change)


    def set_new_index(self):
        ''' Set new index-file name. Never use it! For a testing only... '''
        change = ['Change description', self.index]
        self.index = input('Set index: ')
        change.append(self.index)
        self.changes.append(change)


    def set_attributes(self,
                       path=True,
                       name=True,
                       description=True,
                       key=True,
                       index=False):
        ''' Set a new group parametres for a source '''
        if path: self.set_new_path()
        if name: self.set_new_name()
        if description: self.set_new_description()
        if key: self.set_new_key()
        # !!! Index-file always have a default name "index.json" !!!
        if index: self.set_new_index()



    def open_source(self, name='source', path='./sources'):
        '''
        Open existing index-file and upload source to buffer
        Set a change-counter in zero
        '''
        path_name = path + '/' + name + '/'
        if 'index.json' in os.listdir(path_name):
            with open(path_name + 'index.json', 'r') as index:
                source_attributes = json.load(index)

            # Load attributes
            attributes = source_attributes.get('Attributes')
            self.path = attributes.get('path')
            self.name = attributes.get('name')
            self.description = attributes.get('description')
            self.index = attributes.get('index')

            self.key = attributes.get('key')

            # Load indicators
            self.indicators = source_attributes.get('Indicators')

            # Set log changes
            self.changes = []

            # Working directories
            self.source_directories()

        else:
            print('File "index.json" not exist')


    def close_source(self):
        ''' Remove object '''
        pass


    def save_source(self):
        ''' Save data source to hard drive '''
        header = dict(
                 zip(
                 ['Name of sources',
                  'Description',
                  'Path to index-file'],
                 [self.name,
                  self.description,
                  self.index_path()]))

        attributes = self.attributes()

        indicators = self.indicators

        dictionary = dict(zip(['Header', 'Attributes', 'Indicators'],
                              [header, attributes, indicators]))

        makedir(self.source_path())

        makedir(self.load)
        makedir(self.upload)
        makedir(self.upload_tmp)
        makedir(self.archive)

        with open(self.index_path(), 'w') as file:
            json.dump(dictionary, file, ensure_ascii=False, indent=4)


    def save_source_as(self):
        ''' Save a new copy of data sources(rename and replace it) '''
        self.set_attributes()
        self.save_source()


    def print_info(self):
        ''' Output abstract information about data source '''
        print(self.header())
        print('Attributes:', self.attributes())
        print('Indicators:', self.indicators)


    def check_updates(self):
        list_of_updates = []
        for filename in os.listdir(self.upload):
            if (fnmatch.fnmatch(filename, '*.XLSX') or
                fnmatch.fnmatch(filename, '*.xlsx') or
                fnmatch.fnmatch(filename, '*.XLS') or
                fnmatch.fnmatch(filename, '*.xls')):
                list_of_updates.append(self.upload + filename)
        if len(list_of_updates)>0:
            return list_of_updates
        else:
            return False

# Some actions with Source()-class objects

def create_source():
    src = Source()
    src.set_attributes()
    return src


def open_source(name='source', path='./sources'):
    src = Source()
    src.open_source(name, path)
    return src


def save_source(src):
    src.save_source()


def save_source_as(src):
    src.save_source_as()


def close_source(src):
    del src


class Indicator():
    ''' Indicator of source '''
    def __init__(self, name, description):
        ''' Constructor of indicator '''

        # Attributes from source
        self.source_name = 'source'
        self.source_path = './sources'
        self.source_key = []

        # Attributes of indicator
        self.name = name
        self.description = description
        self.rules = []
        self.positions = None


class Position():
    ''' One position of indicator
        Row: key, value, dt '''

    def __init__(self, key, value, dt):
        self.key = key
        self.value = value
        self.dt = dt
"""
###############################################################################

