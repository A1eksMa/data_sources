# Функция записи лог-файла
def log(message, path = './', filename = '.log', print_message = True):
    log = open(path + filename, 'a')
    log.write(nowtime() + ' ' + str(message) + '\n')
    log.close
    if print_message:
        print(str(message))
    return
