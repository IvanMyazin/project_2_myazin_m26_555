import prompt


def welcome():
    print("Первая попытка запустить проект")
    print("***")
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")

    while True:
        command = prompt.string('Введите команду: ').strip()
        match command:
            case 'exit':
                break
            case 'help':
                print("<command> exit - выйти из программы")
                print("<command> help - справочная информация")
            case _:
                print("Неизвестная команда")

