#Функция перехода из скрипта в режим ввода команд
def command_mode(unit = ''):
    log('#---------- command-mode ----------#', print_message = False)
    command = ''
    while command not in ['q','quit','exit','logout']:
        command = input(unit + ' >>> ')
        log(command, print_message = False)
        try:
            if command not in ['q','quit','exit','logout']: exec(command)
        except Exception as err:
            log(err)
    return
