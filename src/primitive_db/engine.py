import shlex

from prettytable import PrettyTable

from .core import create_table, delete, drop_table, insert, select, update
from .decorators import create_cacher
from .parser import parse_set_clause, parse_values, parse_where_clause
from .utils import load_metadata, load_table_data, save_metadata, save_table_data

FILEPATH = "db_meta.json"


def print_help():
    print("\n***База данных***")
    print("<command> create_table <имя> <столбец:тип> ...")
    print("<command> list_tables")
    print("<command> drop_table <имя>")
    print('<command> insert into <имя> values ("текст", 1, true)')
    print("<command> select from <имя>")
    print("<command> select from <имя> where <столбец> = <значение>")
    print("<command> update <имя> set <столбец> = <значение> where ...")
    print("<command> delete from <имя> where <столбец> = <значение>")
    print("<command> info <имя>")
    print("<command> help")
    print("<command> exit\n")


def print_table(rows, columns):
    if not rows:
        print("Записи не найдены.")
        return

    table = PrettyTable()
    table.field_names = columns

    for row in rows:
        table.add_row([row.get(column) for column in columns])

    print(table)


def get_columns(metadata, table_name):
    columns = []

    for column in metadata[table_name]:
        column_name = column.split(":", 1)[0]
        columns.append(column_name)

    return columns


def run():
    print_help()
    cache_result = create_cacher()

    while True:
        try:
            user_input = input("Введите команду: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nВыход из программы.")
            break

        if not user_input:
            print("Введите команду.")
            continue

        try:
            args = shlex.split(user_input)
            if not args or not args[0]:
                print("Введите команду.")
                continue
        except ValueError as error:
            print(f"Ошибка: {error}")
            continue

        command = args[0]

        try:
            metadata = load_metadata(FILEPATH)
            match command:
                case "create_table":
                    if len(args) < 3:
                        print("Некорректное количество аргументов.")
                        continue

                    table_name = args[1]
                    columns = args[2:]
                    result = create_table(metadata, table_name, columns)
                    if result is not None:
                        save_metadata(FILEPATH, result)
                        cache_result = create_cacher()

                case "list_tables":
                    if not metadata:
                        print("Таблиц нет.")
                    else:
                        for table_name in metadata:
                            print(f"- {table_name}")

                case "drop_table":
                    if len(args) != 2:
                        print("Некорректное количество аргументов.")
                        continue

                    table_name = args[1]
                    result = drop_table(metadata, table_name)
                    if result is not None:
                        save_metadata(FILEPATH, result)
                        cache_result = create_cacher()

                case "insert":
                    if len(args) < 5 or args[1] != "into":
                        print("Некорректная команда insert.")
                        continue

                    before_values, separator, values_text = user_input.partition(
                        " values "
                    )

                    if not separator:
                        print("В команде insert отсутствует values.")
                        continue

                    table_name = before_values.split()[2]

                    if table_name not in metadata:
                        print(f'Ошибка: Таблица "{table_name}" не существует.')
                        continue

                    values = parse_values(values_text)
                    new_data = insert(metadata, table_name, values)

                    if new_data is not None:
                        save_table_data(table_name, new_data)
                        cache_result = create_cacher()

                case "select":
                    if len(args) < 3 or args[1] != "from":
                        print("Некорректная команда select.")
                        continue

                    table_name = args[2]

                    if table_name not in metadata:
                        print(f'Ошибка: Таблица "{table_name}" не существует.')
                        continue

                    where_clause = None

                    if " where " in user_input:
                        condition = user_input.split(" where ", 1)[1]
                        where_clause = parse_where_clause(condition)

                    condition_key = None
                    if where_clause is not None:
                        column = list(where_clause.keys())[0]
                        value = where_clause[column]
                        condition_key = (column, type(value).__name__, value)

                    key = (table_name, condition_key)
                    rows = cache_result(
                        key,
                        lambda: select(load_table_data(table_name), where_clause),
                    )
                    if rows is None:
                        continue
                    columns = get_columns(metadata, table_name)
                    print_table(rows, columns)

                case "update":
                    if " set " not in user_input or " where " not in user_input:
                        print("Некорректная команда update.")
                        continue

                    before_set, conditions = user_input.split(" set ", 1)
                    set_text, where_text = conditions.split(" where ", 1)
                    table_name = before_set.split()[1]

                    if table_name not in metadata:
                        print(f'Ошибка: Таблица "{table_name}" не существует.')
                        continue

                    set_clause = parse_set_clause(set_text)
                    where_clause = parse_where_clause(where_text)
                    table_data = load_table_data(table_name)
                    found_rows = select(table_data, where_clause)

                    if found_rows is None:
                        continue
                    if not found_rows:
                        print("Записи не найдены.")
                        continue

                    result = update(table_data, set_clause, where_clause)
                    if result is not None:
                        save_table_data(table_name, result)
                        cache_result = create_cacher()
                        print(f"Обновлено записей: {len(found_rows)}.")

                case "delete":
                    if len(args) < 6 or args[1] != "from":
                        print("Некорректная команда delete.")
                        continue

                    if " where " not in user_input:
                        print("В команде delete отсутствует where.")
                        continue

                    table_name = args[2]

                    if table_name not in metadata:
                        print(f'Ошибка: Таблица "{table_name}" не существует.')
                        continue

                    condition = user_input.split(" where ", 1)[1]
                    where_clause = parse_where_clause(condition)
                    table_data = load_table_data(table_name)
                    found_rows = select(table_data, where_clause)

                    if found_rows is None:
                        continue
                    if not found_rows:
                        print("Записи не найдены.")
                        continue

                    result = delete(table_data, where_clause)
                    if result is not None:
                        save_table_data(table_name, result)
                        cache_result = create_cacher()
                        print(f"Удалено записей: {len(found_rows)}.")

                case "info":
                    if len(args) != 2:
                        print("Некорректная команда info.")
                        continue

                    table_name = args[1]

                    if table_name not in metadata:
                        print(f'Ошибка: Таблица "{table_name}" не существует.')
                        continue

                    table_data = load_table_data(table_name)
                    columns = ", ".join(metadata[table_name])
                    print(f"Таблица: {table_name}")
                    print(f"Столбцы: {columns}")
                    print(f"Количество записей: {len(table_data)}")

                case "help":
                    print_help()

                case "exit":
                    print("Выход из программы.")
                    break

                case _:
                    print(f"Функции {command} нет. Попробуйте снова.")

        except (IndexError, KeyError, ValueError, OSError) as error:
            print(f"Ошибка: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\nВыход из программы.")
            break
