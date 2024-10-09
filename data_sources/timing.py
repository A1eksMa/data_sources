from datetime import datetime

class Timing():
    """
    """

    def __init__(self, dt = datetime.now()):
        # Date, time in datetime format
        if isinstance(dt, datetime):
            self.dt = dt
        if isinstance(dt, tuple):
            self.dt = datetime.strptime(dt[0], dt[1])

        # Date, time in unix-time format
        self.ut = self.dt.timestamp()


    def dt_string(self, pattern: str = '') -> str:
        if pattern:
            return self.dt.strftime(pattern)
        else:
            return str(self.dt)

    def ut_string(self) -> str:
        return str(int(self.ut*1000000))

    @staticmethod
    def now() -> datetime:
        return datetime.now()

    def set(self,  value: str, pattern: str):
        """
        Looks like a:
        ('2020-01-01 00:00:00', '20'+'%y-%m-%d %H:%M:%S')
        """
        self.dt = datetime.strptime(value, pattern)
        self.ut = self.dt.timestamp()
