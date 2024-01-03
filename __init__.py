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


class Core():
    '''
    It's an abstract class
    '''

    def __init__(self, path, name, description):
        ''' Set up defaults attributes '''

        # Main attributes (single variables)
        self.path = path
        self.name = name
        self.description = description
        self.index = 'index.json'

        # Properties (group variables)
        self.properties = []

    # Aggregate main attributes
    
    def path_name(self):
        ''' Construct a full path to sources index-file '''
        return self.path + self.name + '/'


    def path_name_index(self):
        ''' Construct a full path to sources index-file '''
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
        ''' Construct info '''
        return 'Name: ' + self.name + '\n'\
               'Description: ' + self.description + '\n'\
               'Path to index-file: ' + self.path_name_index() + '\n'


    def info(self):
        ''' Output abstract information about data sources '''
        print(self)
        print('Attributes:', self.main_attributes())
        print('Properties:', self.properties)


    def main_attributes(self):
        ''' Construct dictionary of main attributes '''
        return dict(zip(['path', 'name', 'description', 'index'],
                        [self.path, self.name, self.description, self.index]))
 
    
    def main_dictionary(self):
        ''' Construct object as dictionary '''
        header = self.header()
        attributes = self.main_attributes()
        properties = self.properties
        dictionary = dict(zip(['Header', 'Attributes', 'Properties'],
                              [header, attributes, properties]))
        return dictionary
    

    # Methods, that change main attributes

    def set_new_path(self):
        ''' Set a new path '''
        self.path = input('Set path: ')


    def set_new_name(self):
        ''' Set a new name '''
        self.name = input('Set name: ')


    def set_new_description(self):
        ''' Set a new descripption '''
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

    def close(self):
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

            # Load properties
            self.properties = index_json.get('Properties')

            # Set log changes
            self.changes = []

        else:
            print('File "index.json" not exist')
            

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


        # Change working directories
        self.source_directories()

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

