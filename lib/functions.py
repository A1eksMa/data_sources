def var2str(variable):
    ''' Функция, которая возвращает текстовую строку из имени переменной '''
    return [global_var for global_var in globals() if id(variable) == id(globals()[global_var])][0]


def str2var(str):
    ''' Функция, которая возвращает переменную
    с пустым значением из текстовой строки '''
    locals()[str] = None
    return locals()[str]


def nowtime():
    ''' Функция, которая возвращает 14-значную строку из чисел
    обозначающих текущее время в формате yyyymmddHHMMSS '''
    return datetime.now().strftime('20' + '%y%m%d%H%M%S')


def dirname():
    ''' Функция, которая возвращает относительный путь
    текущего места вызова скрипта
    от корневой директории проекта '''
    return os.path.dirname(os.path.abspath(__file__)).replace(os.getcwd(), '.')


def makedir(path):
    if not os.path.exists(path): os.makedirs(path)


def generate_id(n=10):
    string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    id = ''.join(random.choice(string) for i in range(n))
    return id
