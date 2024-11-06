import json
import shelve
from pathlib import Path

_JSON = 'info.json'
_DATA = 'data' # for file name: `data.db`

class Node():
    """
    Класс Node() - это  соглашение о структуре данных
    и их месторасположении на физическом носителе.

    Объект класса Node() можно предствить как набор словарей:
    - словарь `info`, в котором хранятся статические данные;
    - система вложенных словарей `data`, в которой хранятся динамические данные.

    К статическим данным относятся атрибуты источника, которые:
    а) определяются при создании источника
    б)и не изменяются со временем (название, ключи)
    в) изменяются достаточно редко (путь к источнику, списки атрибутов)
    г) имеют общий информативный характер (описания, статистика, метаданные)

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
    type: "Node",
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

        В случае успешной инициализации создается экземпляр Node() со следующими атрибутами:
        - path:  путь к директории источника данных, физическое расположение данных на жестком диске;
        - info: словарь, прочитанный из файла `info.json`;
        - data: объект shelve, связанный с файлом `data.db`.

        В случае неуспешной инициализации экземпляр Node() не создается, код падает с исключением,
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

        """
        return all(i in self.__dict__.keys() for i in ('path', 'info', 'data'))

    def __repr__(self):
        """
        Показывает общую информацию объекта (тип и метаданные).

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
        Создает новый объект,
        а также структуру всех необходимых для него файлов и папок.

        """
        # create folder
        path = Path(path)
        if not (path.exists() and path.is_dir()):
            path.mkdir(parents=True, exist_ok=True)
        # create `info.json`
        data = {'type': Node(path).class_name(),
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
        return Node(path)

    def class_name(self):
        """
        Возвращает строку с именем класса.

        """
        s = str(type(self))    # smth like a "<class '__main__.Node'>"
        i = s[::-1].find(".")
        s = s[-i:-2]
        return s

    def update_info(self):
        """
        Перезаписывает файл `info.json` информацией из атрибута `self.info`.

        """
        path_json = self.path / _JSON
        with open(path_json, 'w') as file:
            json.dump(self.info, file, ensure_ascii=False, indent=4)

    def keys(self) -> list:
        """
        Возвращает список ключей словаря `data`.
        
        """
        with shelve.open(self.path / 'data') as data:
            return list(data.keys())

    def get_key(self, k: str) -> dict:
        """
        Возвращает элемент словаря `data` по ключу.
        
        """
        with shelve.open(self.path / 'data') as data:
            return data[k]

    def get_keys(self, keys: list) -> list:
        """
        Возвращает список элементов словаря `data` по списку ключей.
        
        """
        with shelve.open(self.path / 'data') as data:
            lst = []
            for i in keys: lst.append(data[i])
            return lst