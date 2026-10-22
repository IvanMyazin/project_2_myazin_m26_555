import shlex

from .core import create_table, drop_table
from .utils import load_metadata, save_metadata

FILEPATH = "db_meta.json"

def print_help():
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print(
        "<command> create_table <имя_таблицы> "
        "<столбец1:тип> <столбец2:тип> ... - создать таблицу"
    )
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def run():
    print_help()

    while True:
         metadata = load_metadata(FILEPATH)

         user_input = input("Введите команду: ").strip()

         if not user_input:
             print("Введите команду.")
             continue

         args = shlex.split(user_input)

         command = args[0]

         match command:
            case 'create_table':
                 if len(args) < 3:
                     print("Некорректное количество аргументов")
                     continue

                 table_name = args[1]
                 columns = args[2:]

                 metadata = create_table(
                     metadata,
                     table_name,
                     columns
                 )

                 save_metadata(FILEPATH, metadata)

            case 'list_tables':
                 if not metadata:
                     print("Таблиц нет.")
                 else:
                     for table_name in metadata:
                         print(f'- {table_name}')

            case 'drop_table':
                if len(args) != 2:
                    print("Некорректное количество аргументов")
                    continue

                table_name = args[1]

                metadata = drop_table(
                    metadata,
                    table_name
                 )

                save_metadata(FILEPATH, metadata)

            case 'help':
                print_help()

            case 'exit':
                 print('Выход из программы')
                 break

            case _:
                 print(f'Функции {command} нет. Попробуйте снова. ')    

         
         
