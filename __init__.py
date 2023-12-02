# import libraries
import pandas as pd
import numpy as np

import json

import datetime as dt
from datetime import datetime
import time as tm

import os
import fnmatch

import plotly.express as px
from dash import Dash, html, dcc

import warnings
warnings.filterwarnings('ignore')

# import functions
path_data_sources = os.path.dirname(os.path.abspath(__file__))
exec(open(path_data_sources +'/lib/functions').read())

class Sources():
    '''
    It's a main class
    '''

    def __init__(self):
        ''' Set up defaults attributes '''

        # Attributes
        self.path = '.'
        self.name = 'sources'
        self.description = 'Default sources'
        self.index = 'index.json'

        # Sources
        self.sources = dict(zip(
            ['One', 'Two', 'Three'],
            ['path_to_one/','path_to_two/','path_to_three/']
            ))

        # log changes to buffer array:
        self.changes = []


    def sources_path(self):
        ''' Construct a full path to sources index-file '''
        return self.path + '/' + self.name + '/'


    def index_path(self):
        ''' Construct a full path to sources index-file '''
        return self.sources_path() + self.index


    def header(self):
        ''' Construct info '''
        return 'Name of sources: ' + self.name + '\n'\
               'Description: ' + self.description + '\n'\
               'Path to index-file: ' + self.index_path() + '\n'


    def attributes(self):
        ''' Construct list of main attributes '''
        return dict(zip(['path', 'name', 'description', 'index'],
                        [self.path, self.name, self.description, self.index]))


    def set_new_path(self):
        ''' Set a new pathname to sources '''
        change = ['Change path', self.path]
        self.path = input('Set path: ')
        change.append(self.path)
        self.changes.append(change)


    def set_new_name(self):
        ''' Set a sources name '''
        change = ['Change name', self.name]
        self.name = input('Set name: ')
        change.append(self.name)
        self.changes.append(change)


    def set_new_description(self):
        ''' Set a more abroad descripption of sources '''
        change = ['Change description', self.description]
        self.description = input('Input description of sources: ')
        change.append(self.description)
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
                       index=False):
        ''' Set a new group parametres for a sources '''
        if path: self.set_new_path()
        if name: self.set_new_name()
        if description: self.set_new_description()
        # !!! Index-file always have a default name "index.json" !!!
        if index: self.set_new_index()



    def open_sources(self, name='sources', path='.'):
        '''
        Open existing index-file and upload sources to buffer
        Set a change-counter in zero
        '''
        path_name = path + '/' + name + '/'
        if 'index.json' in os.listdir(path_name):
            with open(path_name + 'index.json', 'r') as index:
                sources_attributes = json.load(index)

            # Load attributes
            attributes = sources_attributes.get('Attributes')
            self.path = attributes.get('path')
            self.name = attributes.get('name')
            self.description = attributes.get('description')
            self.index = attributes.get('index')

            # Load sources
            self.sources = sources_attributes.get('Sources')

            # Set log changes
            self.changes = []

        else:
            print('File "index.json" not exist')


    def close_sources(self):
        ''' Remove object '''
        pass


    def save_sources(self):
        ''' Save data sources to hard drive '''
        header = dict(
                 zip(
                 ['Name of sources',
                  'Description',
                  'Path to index-file'],
                 [self.name,
                  self.description,
                  self.index_path()]))

        attributes = self.attributes()

        sources = self.sources

        dictionary = dict(zip(['Header', 'Attributes', 'Sources'],
                              [header, attributes, sources]))

        makedir(self.sources_path())
        with open(self.index_path(), 'w') as file:
            json.dump(dictionary, file, ensure_ascii=False, indent=4)


    def save_sources_as(self):
        ''' Save a new copy of data sources (rename and replace it) '''
        self.set_attributes()
        self.save_sources()


    def print_info(self):
        ''' Output abstract information about data sources '''
        print(self.header())
        print('Attributes:', self.attributes())
        print('Sources:', self.sources)


# Some actions with Sources()-class objects

def create_sources():
    srcs = Sources()
    srcs.set_attributes()
    return srcs


def open_sources(name='sources', path='.'):
    srcs = Sources()
    srcs.open_sources(name, path)
    return srcs


def save_sources(srcs):
    srcs.save_sources()


def save_sources_as(srcs):
    srcs.save_sources_as()


def close_sources(srcs):
    del srcs

class Source():
    '''
    This class working with  particular data source
    Source contains "indicators" and their history
    Every source have got a "key": one or more "indicators"
    It used as primary key for updating data source
    '''

    def __init__(self):
        ''' Set up defaults attributes of source'''

        # Attributes
        self.path = './sources'
        self.name = 'source'
        self.description = 'Default source'
        self.index = 'index.json'

        # Key (unique attribute or unique combination attributes)
        self.key = []

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
        change.append(self.path)
        self.changes.append(change)


    def set_new_name(self):
        ''' Set a source name '''
        change = ['Change name', self.name]
        self.name = input('Set name: ')
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

