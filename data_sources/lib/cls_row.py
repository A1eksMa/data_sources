import shelve
from lib.cls_node import Node
from lib.cls_times import Times
from lib.cls_excel import ExcelFile


class Row(Node):
    """
    Класс Row() описывает структуру "сырых" данных.

    В атрибут `data` класса Row() записываются "точки обновления" данных:
    при этом:
        ключ - время получения новых данных;
        значение - словарь с данными.

    Общая идея класса Row() - это что-то вроде  git-а,
    где каждая "точка обновления" - это коммит,
    передвигаясь от начальной точки по порядку можно получить
    состояние на любой момент времени ("машина времени").

    Задача класса Row() - хранить исходники информации загруженных
    в систему источников данных - сырые строки, в виде "квадратных таблиц".
    
    Под "квадратной таблицей" понимается таблица, состоящая из одной строки
    заголовка и любого количества строк с данными.
    Заголовок такой таблицы содержит показатели источника данных ("indicators").
    Строки с данными содержат значения показателей.

    В структурах данных python под "квадратной таблицей" понимается словарь,
    ключи которого - это оказатели источника данных ("indicators"),
    значения - списки одинаковой длины (значения показателей).
    
    В перспективе здесь же будут загрузчики из разного типа файлов,
    или файлов с разной структурой, обрабатываемые с помощью хэндлеров,
    возможно какие-то функции изначальной фильтрации и предобработки,
    а также функции архивации, восстановления и удаления исходных данных.
        
    """

    def upload(self, file_path):
        """
        Метод `upload` создает новую "точку обновления" - кадр данных,
        на момент времени его получения. Он же: "окно данных" - "dataframe".

        В качестве аргумента метод принимает путь к файлу с данными,
        из которого будет получен словарь с данными.

        Полученный словарь записывается в атрибут `data` под ключом
        даты-времени в формате unixtime в милисикундах.
        
        """
        
        dt = Times()
        with shelve.open(self.path / 'data') as data:
            data[dt.uts] = ExcelFile(file_path).dict()

    def get_data(self, d: dict) -> dict:
        """
        Метод `get data` из каждой "квадратной таблицы" с сырыми данными `d`
        собирает двухуровневый словарь `data`.

        На первом уровне словара `data` - показатели ("indicators").
        На втором уровне для каждого показателя формируется пара ключ-значение, где:
            ключ - кортеж с рекомбинацией ключевых полей для источника данных,
            значение - соответствующее ему значение показателя.
        
        """
        
        # Get object keys
        keys = self.info['keys']
        
        # Check keys not empty and keys exist
        if not keys: raise Error("Required keys is empty!")
            
        for k in keys:
            if k not in d.keys(): 
                raise Error("Required key is not found!")

        # Create keys list
        keys_list = []
        for i in range(len(d[keys[0]])):
            
            t = []
            for k in keys:
                t.append(d[k][i])
            keys_list.append(t)
        
        # Convert keys to tuple
        keys_list = [tuple(i) for i in keys_list]

        # Check elements in keys_list is unique
        if len(set(keys_list)) != len(keys_list):
            raise Error("Value of key is not unique!")
        
        # Construct dataset
        data = {}
        for k in d.keys():
            data[k] = {}
            for i in range(len(keys_list)):
                data[k][keys_list[i]] = d[k][i]
        
        return data
        
