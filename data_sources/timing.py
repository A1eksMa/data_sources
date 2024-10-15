from datetime import datetime

class Timing():
    """
    Вспомогательный класс, для обработки показателей даты/времени.
    Обеспечивает некоторый полиморфизм входных данных (при инциализации),
    по умолчанию инициализируется значением текущей даты/времени.

    Объект гарантировано содержит атрибуты даты/времени в формате:
    dt: datetime
    ut: unix-time
    dts: datetime в формате строки
    uts: unix-time в формате строкового отображения целого числа (милисекунды)
    uti: unix-time в формате целого числа (в милисикундах)

    """

    def __init__(self, dt = datetime.now()):
        """
        Инициализируется аргументом в формате datetime.
        По умолчанию - текущим значением даты/времени.

        Если тип переданного аргумента отличается от datetime,
        пытается конвертировать его в тип datetime,
        исходя из предположения, что переданное в качестве аргумента значение
        совпадает с форматом одного из атрибутов.

        Также можно инициализировать объект, передав кортеж из двух элементов,
        первый из которых - строковое выражение даты/времени,
        второе - шаблон для конвертации.
        Для примера:
        ('2020-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')

        """
        if not dt: raise AttributeError("Initialization with False argument.")

        # Date, time in datetime format
        # from datetime
        if isinstance(dt, datetime):
            self.dt = dt
        # from tuple
        # Tuple should be looks like a (value: str, pattern: str).
        if isinstance(dt, tuple):
            if not dt[0]:
                raise AttributeError("Initialization with False argument.")
            self.dt = datetime.strptime(dt[0], dt[1])
        # from string
        if isinstance(dt, str):
            if dt.isnumeric():
                dt = int(dt)
            else:
                self.dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S.%f')
        # from integer
        if isinstance(dt, int):
            dt = str(dt)
            dt = dt[:-6] + '.' + dt[-6]
            dt = float(dt)
            self.dt = datetime.fromtimestamp(dt)

        # Date, time in unix-time format
        self.ut = self.dt.timestamp()
        # Other formats
        self.dts = self.dt_string()
        self.uts = self.ut_string()
        self.uti = self.ut_integer()

    def dt_string(self) -> str:
        return str(self.dt)

    def ut_string(self) -> str:
        return str(int(self.ut*1000000))

    def ut_integer(self) -> int:
        return int(self.ut*1000000)
