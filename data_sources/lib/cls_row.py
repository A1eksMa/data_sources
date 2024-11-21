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
    Заголовок такой таблицы содержит показатели ("indicators") источника данных.
    Строки с данными содержат значения показателей.

    В структурах данных python под "квадратной таблицей" понимается словарь,
    ключи которого - это показатели источника данных ("indicators"),
    значения - списки одинаковой длины (значения показателей).
    
    В перспективе здесь же будут загрузчики из разного типа файлов,
    или файлов с разной структурой, обрабатываемые с помощью хэндлеров,
    возможно какие-то функции изначальной фильтрации и предобработки,
    а также функции архивации, восстановления и удаления исходных данных.
        
    """
    
    def __init__(self, path: str):
        """
        Метод __init__ родительского класса устанавливает для
        нового вновь создаваемого объекта структуру файлов и папок,
        в том числе словарь `data` для хранения данных на жестком диске
        и словарь `info` для хранения метаданных.
        
        """
        super().__init__(path)
        
        with shelve.open(self.path / 'start') as start:
            # атрибут   хранит первоначальную "точку обновления"
            # самый первый (из известных) момент загрузки данных
            self.start = start
            
        with shelve.open(self.path / 'final') as final:
            # атрибут `final` хранит итоговое состояние,
            # с учетом всех загруженных "точек обновления"
            self.final = final

    def get_start_dt(self):
        with shelve.open(self.path / 'start') as start:
            return start['dt']

    def get_start_data(self):
        with shelve.open(self.path / 'start') as start:
            return start['data']
            
    def get_final_dt(self):
        with shelve.open(self.path / 'final') as final:
            return final['dt']

    def get_final_data(self):
        with shelve.open(self.path / 'final') as final:
            return final['data']   
 
    def upload(self, file_path):
        """
        Метод `upload` создает новую "точку обновления" - кадр данных,
        на момент времени его получения. Он же: "окно данных", он же "dataframe".

        В качестве аргумента метод принимает путь к файлу с данными,
        из которого будет получен словарь с данными.

        Полученный словарь записывается в атрибут `data` под ключом
        даты-времени в формате unixtime в милисикундах.
        
        """
        # фиксируем время обновления
        dt = Times()

        # получаем данные для обновления в виде словаря
        d = ExcelFile(file_path).dict()

        # если это первоначальная точка обновления,
        # записываем данные в атрибут `start`
        with shelve.open(self.path / 'start') as start:
            self.start = start
            if not start:
                self.start['dt'] = dt.uts
                self.start['data'] = self.get_data(d)

        # записываем данные обновления в атрибут `data`
        with shelve.open(self.path / 'data') as data:
            data[dt.uts] = d

        # для формирования итогового состояния
        # с учетом информации предыдущих "точек обновления",
        # накатываем данные поверх ранее записаных в атрибут `final`
        with shelve.open(self.path / 'final') as final:
            self.final = final
            self.final['dt'] = dt.uts
            self.final['data'] = self.get_data(d)
            

    def get_data(self, d: dict) -> dict:
        """
        Метод `get data` из каждой "квадратной таблицы" с сырыми данными `d`
        собирает двухуровневый словарь `data`.

        На первом уровне словара `data` - показатели ("indicators").
        На втором уровне для каждого показателя формируется пара ключ-значение, где:
            ключ - кортеж с рекомбинацией ключевых полей для источника данных,
            значение - соответствующее ему значение показателя.

        В результате мы имеем следующую структуру данных:
        
        data = {
                Indicator_1 : { (key_1, key_2, key_3) : value,
                                (key_1, key_2, key_3) : value,
                                (key_1, key_2, key_3) : value,
                }
                Indicator_2 : { (key_1, key_2, key_3) : value,
                                (key_1, key_2, key_3) : value,
                                (key_1, key_2, key_3) : value,
                
                }
                Indicator_3 : { (key_1, key_2, key_3) : value,
                                (key_1, key_2, key_3) : value,
                                (key_1, key_2, key_3) : value,
                
                }
                
                ...
            }

            Метод `get_data` выбрасывает ошибку и завершает программу,
            если в исходных данных отсутствуют требуемые для построения структуры ключи
            (перечень требуемых ключей установлен в свойствах источника данных).
        
        """
        
        # Get object keys
        keys = self.info['keys']
        
        # Check keys not empty and keys exist in row data
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

        def get_dataframe(self, dt):
            """

            """
            pass
        
