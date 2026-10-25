from .decorators import confirm_action, handle_db_errors, log_time
from .utils import load_table_data

ALLOWED_TYPES = ["int", "str", "bool"]


@handle_db_errors
def create_table(metadata, table_name, columns):
    if table_name in metadata:
        raise ValueError(f'Таблица "{table_name}" уже существует.')

    new_columns = ["ID:int"]

    for column in columns:
        if ":" not in column:
            raise ValueError(f"Некорректное значение: {column}.")

        column_name, column_type = column.split(":", 1)

        if column_type not in ALLOWED_TYPES:
            raise ValueError(f"Некорректный тип: {column_type}.")

        if not column_name or any(
            existing.split(":", 1)[0] == column_name for existing in new_columns
        ):
            raise ValueError(f"Пустой или повторяющийся столбец: {column_name}.")

        new_columns.append(column)

    metadata[table_name] = new_columns

    columns_text = ", ".join(new_columns)

    print(f'Таблица "{table_name}" успешно создана со столбцами: {columns_text}')

    return metadata


@handle_db_errors
@confirm_action("удаление таблицы")
def drop_table(metadata, table_name):
    if table_name not in metadata:
        raise KeyError(table_name)

    del metadata[table_name]

    print(f'Таблица "{table_name}" успешно удалена.')

    return metadata


@handle_db_errors
@log_time
def insert(metadata, table_name, values):
    if table_name not in metadata:
        raise KeyError(table_name)

    table_data = load_table_data(table_name)
    columns = metadata[table_name][1:]

    if len(values) != len(columns):
        raise ValueError("Некорректное количество значений.")

    new_id = 1

    if table_data:
        new_id = max(row["ID"] for row in table_data) + 1

    new_row = {"ID": new_id}

    for column, value in zip(columns, values):
        column_name, column_type = column.split(":", 1)

        if type(value).__name__ != column_type:
            raise ValueError(f"Некорректный тип значения для столбца {column_name}.")

        new_row[column_name] = value

    table_data.append(new_row)

    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')

    return table_data


@handle_db_errors
@log_time
def select(table_data, where_clause=None):
    if where_clause is None:
        return table_data

    if len(where_clause) != 1:
        raise ValueError("Укажите одно условие where.")

    column = list(where_clause.keys())[0]
    value = where_clause[column]
    selected_rows = []

    for row in table_data:
        if row[column] == value:
            selected_rows.append(row)

    return selected_rows


@handle_db_errors
def update(table_data, set_clause, where_clause):
    if len(set_clause) != 1 or len(where_clause) != 1:
        raise ValueError("Укажите один столбец set и одно условие where.")

    where_column = list(where_clause.keys())[0]
    where_value = where_clause[where_column]

    set_column = list(set_clause.keys())[0]
    new_value = set_clause[set_column]

    if set_column == "ID":
        raise ValueError("ID создаётся автоматически и не изменяется.")

    # Проверяем все записи до изменения, чтобы ошибка не оставила часть изменений.
    for row in table_data:
        if where_column not in row:
            raise KeyError(where_column)
        if set_column not in row:
            raise KeyError(set_column)
        if type(row[set_column]) is not type(new_value):
            raise ValueError(f"Некорректный тип значения для столбца {set_column}.")

    for row in table_data:
        if row[where_column] == where_value:
            row[set_column] = new_value

    return table_data


@handle_db_errors
@confirm_action("удаление записей")
def delete(table_data, where_clause):
    if len(where_clause) != 1:
        raise ValueError("Укажите одно условие where.")

    column = list(where_clause.keys())[0]
    value = where_clause[column]
    remaining_rows = []

    for row in table_data:
        if row[column] != value:
            remaining_rows.append(row)

    return remaining_rows
