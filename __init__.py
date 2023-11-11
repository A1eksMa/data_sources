# Импортируем библиотеки и зависимоcти python
import numpy as np
import pandas as pd

import json

import datetime as dt
from datetime import datetime
import time as tm

import os
import fnmatch

import warnings
warnings.filterwarnings('ignore')

class Sources:
    """
    Класс 'Источники данных'
    Хранит информацию о всех источниках данных и их месторасположении

    Класс 'Sources' является родительским по отношению к классу 'Source' (src)

    Методы класса 'Sources' оперируют с объектами класса 'Source' (src)
    и позволяют:
    - добавлять,
    - удалять,
    - изменять,
    - переименовывать,
    - перемещать
    объекты класса 'Source' (src), а также получать общую информацию о них

    Методы класса работают со словарем, вида:
    {
    'source_1': '/path_to_source_1/',
    'source_2': '/path_to_source_2/',
    'source_3': '/path_to_source_3/'
    }

    Каждой записи словаря соответствует экземпляр класса Source (src)
    Действия методов класса 'Sources' выполняются как над записями словаря,
    так и над сопоставленным с ним объектом класса Source (src)

    При выполнении методов происходит валидация данных словаря

    Статические данные словаря хранятся в json-файле:
    index.json, расположенному в рабочей директории 'path'
    (по умолчанию './sources')

    В ту же директорию происходит логирование всей действий,
    совершаемых методами класса.

    """

    def __init__(self):
        """
        Устанавливает рабочую директорию по умолчанию
        и  создает пустой словарь со списком источников
        при инициализации объектов
        """
        self.path = './sources/'
        self.sources = {'': ''}
        return


    def set_path(self, new_path):
        """
        Метод устанавливает путь к рабочей директории 'path'
        """
        # Валидация указанного пути
        pass

        # Проверка, что указанный путь существует
        pass

        # Если указанный каталог не существует - он будет создан
        pass

        self.path = new_path
        return self.path


    def get_path(self):
        """
        Метод возвращает установленный путь к рабочей директории 'path'
        """
        return print(self.path)


    def open_sources(self):
        """
        Метод открывает словарь со списком источников из рабочей директории
        """
        # попытка найти и загрузить файл index.json из рабочей директории
        if 'index.json' in os.listdir(self.path):
            with open(self.path + 'index.json', 'r') as fl_json:
                index_json = json.load(fl_json)
            self.sources = index_json
        else:
            print('Не удалось получить доступ к источникам даных')


    def create_sources(self, sources_name):
        '''
        Создает новый объект Sources (с рабочей директорией по умолчанию)
        и создает в нейновый пустой словарь для хранения данных
        '''
        sources_name = self.Sources()


    def save_sources(self):
        '''

        '''
        pass


    def close(self):
        '''

        '''
        pass
