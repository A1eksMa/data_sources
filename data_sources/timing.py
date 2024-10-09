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
    uti: unix-time в формате целого числа (в милисикундах)
    uts: unix-time в формате строкового отображения целого числа (в милисикундах)
    
    """

    def __init__(self, dt = datetime.now()):
        # Date, time in datetime format
        # from datetime
        if isinstance(dt, datetime):
            self.dt = dt
        # from tuple
        # Tuple should be looks like a (value: str, pattern: str).
        # For example:
        # ('2020-01-01 00:00:00', '20'+'%y-%m-%d %H:%M:%S')
        if isinstance(dt, tuple): 
            self.dt = datetime.strptime(dt[0], dt[1])
        # from string
        if isinstance(dt, str):
            pass

        # Date, time in unix-time format
        self.ut = self.dt.timestamp()
        # Other formats
        self.dts = self.dt_string()
        self.uts = self.ut_string()
        self.uti = self.ut_integer()
        
    def dt_string(self, pattern: str = '') -> str:
        if pattern:
            return self.dt.strftime(pattern)
        else:
            return str(self.dt)

    def ut_string(self) -> str:
        return str(int(self.ut*1000000))

    def ut_integer(self) -> int:
        return int(self.ut*1000000)
