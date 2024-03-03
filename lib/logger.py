# Функция записи лог-файла
def log(message, path = './', filename = '.log', print_message = True):
    log = open(path + filename, 'a')
    log.write(nowtime() + ' ' + str(message) + '\n')
    log.close
    if print_message:
        print(str(message))
    return


# LOGGING
# Set base config logging
logging.basicConfig(level=logging.DEBUG, filename="main.log",filemode="w",
                     format="%(asctime)s %(levelname)s %(message)s")

# Create a logger with logging
logger = logging.getLogger('main_logger')
logger.setLevel(logging.DEBUG)

# Create file handler
file_handler = logging.FileHandler('main.log')
file_handler.setLevel(logging.DEBUG)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
