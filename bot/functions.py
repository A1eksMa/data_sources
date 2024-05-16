import pathlib
import hashlib
import json
from datetime import datetime
from collections import defaultdict

def nowtime():
    ''' Return string of current time: yyyymmddHHMMSS '''
    return datetime.now().strftime('20' + '%y%m%d%H%M%S')

def get_file_extension(path):
    return path[-path[::-1].index('.')-1:]

def get_file_name(path):
    return path[-path[::-1].index('/'):]

def walk(path):
    ''' This function is designed to retrieve a list of files
    within a specified directory path '''
    for child in path.glob('*'):
        if child.is_dir():
            yield from walk(child)
        else:
            yield str(child)

def get_file_list(path):
    ''' It utilizes walk() function to traverse the directory structure
    and collect the file paths into a list'''
    return [i for i in walk(pathlib.Path(path))]

def get_file_hash(file_path):
    ''' Generates a hash value for a file using the SHA-256 algorithm '''
    with open(file_path, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    return file_hash

def get_file_attributes(path):
    ''' Retrieves file attributes such as file paths
    and their corresponding hashes within a specified directory '''
    return {file: (pathlib.Path(i), get_hash(i)) for i in get_file_list(path)}

def bitwise_file_compare(file1, file2):
    ''' The function compares the binary content of two files
    to determine if they are identical '''
    with open(file1, "rb") as f1, open(file2, "rb") as f2:
        return f1.read() == f2.read()

def write_json(path_json, data):
    ''' Writes JSON data to a file '''
    with open(path_json, 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def read_json(path_json):
    ''' Reads a JSON file and returns its contents as a dictionary '''
    with open(path_json, 'r') as file:
        data = json.load(file)
    return dict(data)


class Photo:
    def __init__(self):
            setattr(self,
                    f"{self.__class__.__name__.lower()}",
                    defaultdict(lambda: None))

class TG_Chat_Info(Photo):

    def get_tg_chat_info(self, chat_info):
        self.tg_chat_info.update({i[0]: i[1] for i in dict(chat_info).items()})

class TG_Msge_Info(Photo):

    def get_tg_msge_info(self, msge_info):
        self.tg_msge_info.update({i[0]: i[1] for i in dict(msge_info).items()})

    def get_msge_id(self, id):
        if id:
            self.tg_msge_info.update({'message_id': id})

    def get_msge_date(self, date):
        if date:
            self.tg_msge_info.update({'date': date})

    def get_msge_caption(self, caption):
        if caption:
            self.tg_msge_info.update({'caption': caption})

class TG_User_Info(Photo):

    def get_tg_user_info(self, user_info):
        self.tg_user_info.update({i[0]: i[1] for i in dict(user_info).items()})

class TG_Foto_Info(Photo):

    def get_tg_foto_info(self, foto_info):
        self.tg_foto_info.update({i[0]: i[1] for i in dict(foto_info).items()})

class TG_File_Info(Photo):

    def get_tg_file_info(self, file_info):
        self.tg_file_info.update({i[0]: i[1] for i in dict(file_info).items()})

class TG_Session_Info(Photo):
    pass

class File_Path(Photo):
    pass

class User_Session(TG_Chat_Info,
                   TG_Msge_Info,
                   TG_User_Info,
                   TG_Foto_Info,
                   TG_File_Info,
                   TG_Session_Info,
                   File_Path):
    def __init__(self):
        self.tg_chat_info = TG_Chat_Info().tg_chat_info
        self.tg_msge_info = TG_Msge_Info().tg_msge_info
        self.tg_user_info = TG_User_Info().tg_user_info
        self.tg_foto_info = TG_Foto_Info().tg_foto_info
        self.tg_file_info = TG_File_Info().tg_file_info
        self.tg_session_info = TG_Session_Info().tg_session_info
        self.file_path = File_Path().file_path
