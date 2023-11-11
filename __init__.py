# import libraries
exec(open('./lib/libraries').read())
exec(open('./lib/functions').read())

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


    def index_path(self):
        ''' Construct a full path to sources index-file '''
        return self.path + '/' + self.name + '/' + self.index


    def header(self):
        ''' Construct info '''
        return 'Name of sources: ' + self.name + '\n'\
               'Description: ' + self.description + '\n'\
               'Path to index-file: ' + self.index_path() + '\n'


    def attributes(self):
        ''' Construct list of main attributes '''
        return dict(zip(['path', 'name', 'description', 'index'], 
                        [self.path, self.name, self.description, self.index]))


    def new_path(self):
        ''' Set a new pathname to sources '''
        change = ['Change path', self.path]
        self.path = input('Set path: ')
        change.append(self.path)
        self.changes.append(change)


    def new_name(self):
        ''' Set a sources name '''
        change = ['Change name', self.name]
        self.name = input('Set name: ')
        change.append(self.name)
        self.changes.append(change)


    def new_description(self):
        ''' Set a more abroad descripption of sources '''
        change = ['Change description', self.description]
        self.description = input('Input description of sources: ')
        change.append(self.description)
        self.changes.append(change)

    def new_index(self):
        ''' Set new index-file name. Never use it! For a testing only... '''
        change = ['Change description', self.index]
        self.index = input('Set index: ')
        change.append(self.index)
        self.changes.append(change)


    def create(self):
        ''' Set a new group parametres for a sources '''
        self.new_path()
        self.new_name()
        self.new_description()
        # !!! Index-file always have a default name "index.json" !!!
        # self.new_index()



    def open(self, name='sources', path='.'):
        '''
        Open existing index-file and upload sources to buffer
        Set a change-counter
        '''
        path_name = path + '/' + name + '/'
        if 'index.json' in os.listdir(path_name):
            with open(path_name + 'index.json', 'r') as index:
                sources_attributes = json.load(index)

            # Load attributes
            self.path = sources_attributes.get('Attributes').get('path')
            self.name = sources_attributes.get('Attributes').get('name')
            self.description = sources_attributes.get('Attributes').get('description')
            self.index = sources_attributes.get('Attributes').get('index')

            # Load sources
            self.sources = sources_attributes.get('Sources')

            # Set log changes
            self.changes = []

        else:
            print('File "index.json" not exist')


    def close(self):
        ''' Remove object '''
        pass


    def save(self):
        ''' Save data from buffer to hard drive '''
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

        dictionary = dict(zip(['Header', 'Attributes', 'Sources'], [header, attributes, sources]))

        with open(self.index_path(), 'w') as file:
            json.dump(dictionary, file, ensure_ascii=False, indent=4)


    def save_as(self):
        ''' Save a new copy of data sources (rename and replace it) '''
        self.create()
        self.save()


    def print_info(self):
        ''' Output abstract information about data sources '''
        print(self.header())
        print('Attributes:', self.attributes())
        print('Sources:', self.sources)
