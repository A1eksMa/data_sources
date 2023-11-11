# Функция, которая возвращает текстовую строку из имени переменной
def var2str(variable):
    return [global_var for global_var in globals() if id(variable) == id(globals()[global_var])][0]

# Функция, которая возвращает переменную с пустым значением из текстовой строки
def str2var(str):
    locals()[str] = None
    return locals()[str]

# Функция, которая возвращает 14-значную строку из чисел
# обозначающих текущее время в формате yyyymmddHHMMSS
def nowtime():
    return datetime.now().strftime('20' + '%y%m%d%H%M%S')

# Функция, которая возвращает относительный путь
# текущего места вызова скрипта
# от корневой директории проекта
def dirname():
    return os.path.dirname(os.path.abspath(__file__)).replace(os.getcwd(), '.')
