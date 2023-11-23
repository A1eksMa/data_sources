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

        with open(self.index_path(), 'w') as file:
            json.dump(dictionary, file, ensure_ascii=False, indent=4)


    def save_sources_as(self):
        ''' Save a new copy of data sources (rename and replace it) '''
        self.set_attributes()
        self.save()


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


class Source(Sources):
    def __init__(self):
        ''' Set up defaults attributes '''

        # Attributes
        super().__init__()
        self.name = None
        self.description = None
        self.path = './sources'
