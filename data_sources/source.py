import json
import shelve
from pathlib import Path

_JSON = 'info.json'
_DATA = 'data' # for file name: `data.db`

class Source():
    """
    Класс Source() - это  соглашение о структуре данных
    и их месторасположении на физическом носителе.

    Объект класса Source() можно предствить как набор словарей:
    - словарь `info`, в котором хранятся статические данные;
    - система вложенных словарей `data`, в которой хранятся динамические данные.
    
    К статическим данным относятся атрибуты источника, которые:
    а) определяются при создании источника и не изменяются со временем (название, ключи)
    б) изменяются достаточно редко (путь к источнику, списки атрибутов)
    в) имеют общий информативный характер (описания, статистика, метаданные)
    
    К динамическим данным относятся значения показателей (indicators) источника данных.
    При этом: каждое из таких значений может быть представлено динамическим рядом
    (последовательностью, в отношении каждого элемента которой выполняются операции ранжирования:
    >&<&!=). В простейшем случае динамический ряд представлен показателями типа datetime,
    отражающими время получения информации о значении показателя источника данных.

    Для операций с данными используются ТОЛЬКО нативные структуры python
    (без необходимости подключения внешних модулей или библиотек)!
    
    Для записи и хранения данных используется  директория, указанная при инициализации объекта.

    Для записи и хранения статических данных используется модуль json,
    файл `info.json` расположен в директории, указанной при инициализации объекта.
    При каждом изменении статических данных файл обновляется (перезаписывается).

    Для записи и хранения динамических данных используется модуль shelve,
    файл `data.db` расположеный в директории, указанной при инициализации объекта.

    `info` looks like a:
    {
    type: "Source",
    name: String,
    description: String,
    keys: tuple(str, str, str),
    indicators: list[str, str, str],
    }
    

    `data` looks like a:
    {
    (key1, key2): { datetime(i-1): indicator,
                   datetime(i): indicator,
                   datetime(i+1): indicator,
                 }
    }
    
    """

    def __init__(self, path: str):
        """
        Для инициации объекта передается путь к источнику данных.
        При инициации объекта происходит ряд проверок:
        - валидация пути (путь к папке существует);
        - валидация файловой структуры (папка содержит файлы, необходимые для инициации);
        - валидация данных (в случае отсутствия файлов для записи и хранения данных источника,
        они будут созданы).

        В случае успешной инициализации создается экземпляр Source() со следующими атрибутами:
        - path:  путь к директории источника данных, физическое расположение данных на жестком диске;
        - info: словарь, прочитанный из файла `info.json`;
        - data: объект shelve, связанный с файлом `data.db`.

        В случае неуспешной инициализации экземпляр Source() не создается, код падает с исключением,
        либо создается пустой объект (объект без перечисленных выше атрибутов).
        
        """
        if path and Path(path).is_dir():
            self.path = Path(path)

            path_json = self.path / _JSON

            if path_json.exists():
                with open(path_json, 'r') as file:
                    self.info = json.load(file)
                    if 'keys' in self.info.keys():
                        self.info['keys'] = tuple(self.info['keys'])

                    if self.info['type'] == self.class_name():

                        path_data = self.path / _DATA

                        with shelve.open(path_data) as data:
                            self.data = data

    def __bool__(self) -> bool:
        """
        Функция проверяет, является ли объект пустым.
        В общем случае проверяет наличие у объекта всех трех атрибутов:
        - path;
        - info;
        - data.
        
        True instance have all of three valid atributes.
        """
        return all(i in self.__dict__.keys() for i in ('path', 'info', 'data'))

    def __repr__(self):
        """
        Print general info about instance.
        """
        s = str(type(self)) + "\n"
        for i, val in self.info.items():
            s += str(i) + ": " + str(val) +"\n"
        return s

    @staticmethod
    def new(path: str,
            name: str,
            description = str(),
            keys = tuple(),
            indicators = list(),
            ):
        """
        Create a new instance with a folder and files structure.
        """
        # create folder
        path = Path(path)
        if not (path.exists() and path.is_dir()):
            path.mkdir(parents=True, exist_ok=True)
        # create `info.json`
        data = {'type': Source(path).class_name(),
                'name': name,
                'description': description,
                'keys': keys,
                'indicators': indicators,
                }
        path_json = path / _JSON
        with open(path_json, 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        # create `data.db`
        path_data = path / str(_DATA + '.db')
        with shelve.open(path / _DATA) as data:
            pass
        return Source(path)

    def class_name(self):
        """
        Return name of class as a String.
        """
        s = str(type(self))    # smth like a "<class '__main__.Source'>"
        i = s[::-1].find(".")
        s = s[-i:-2]
        return s

    def update_info(self):
        """
        Rewrite `info.json` file from `self.info` atribute.
        """
        path_json = self.path / _JSON
        with open(path_json, 'w') as file:
            json.dump(self.info, file, ensure_ascii=False, indent=4)
