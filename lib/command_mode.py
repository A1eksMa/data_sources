#Функция перехода из скрипта в режим ввода команд
def command_mode(unit = ''):
    log('#---------- command-mode ----------#', print_message = False)
    command = ''
    while command != 'exit':
        command = input(unit + ' >>> ')
        log(command, print_message = False)
        try:
            exec(command)
        except:
            log('Error')
    return
