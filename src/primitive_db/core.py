from .utils import load_table_data

ALLOWED_TYPES = ["int", "str", "bool"]


def create_table(metadata, table_name, columns):
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует!')
        return metadata

    new_columns = ["ID:int"]

    for column in columns:
        if ":" not in column:
            print(f"Некорректное значение: {column}. Попробуйте снова.")
            return metadata

        column_name, column_type = column.split(":", 1)

        if column_type not in ALLOWED_TYPES:
            print(f"Некорректное значение: {column_type}. Попробуйте снова.")
            return metadata

        new_columns.append(column)

    metadata[table_name] = new_columns

    columns_text = ", ".join(new_columns)

    print(
        f'Таблица "{table_name}" успешно создана '
        f"со столбцами: {columns_text}"
    )

    return metadata

def drop_table(metadata, table_name):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]

    print(f'Таблица "{table_name}" успешно удалена.')

    return metadata


def insert(metadata, table_name, values):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return []

    table_data = load_table_data(table_name)
    columns = metadata[table_name][1:]

    if len(values) != len(columns):
        print("Некорректное количество значений.")
        return table_data

    new_id = 1

    if table_data:
        new_id = max(row["ID"] for row in table_data) + 1

    new_row = {"ID": new_id}

    for column, value in zip(columns, values):
        column_name, column_type = column.split(":", 1)

        if type(value).__name__ != column_type:
            print(f"Некорректный тип значения для столбца {column_name}.")
            return table_data

        new_row[column_name] = value

    table_data.append(new_row)

    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')

    return table_data


def select(table_data, where_clause=None):
    if where_clause is None:
        return table_data

    column = list(where_clause.keys())[0]
    value = where_clause[column]
    selected_rows = []

    for row in table_data:
        if row.get(column) == value:
            selected_rows.append(row)

    return selected_rows


def update(table_data, set_clause, where_clause):
    where_column = list(where_clause.keys())[0]
    where_value = where_clause[where_column]

    set_column = list(set_clause.keys())[0]
    new_value = set_clause[set_column]

    for row in table_data:
        if row.get(where_column) == where_value:
            row[set_column] = new_value

    return table_data


def delete(table_data, where_clause):
    column = list(where_clause.keys())[0]
    value = where_clause[column]
    remaining_rows = []

    for row in table_data:
        if row.get(column) != value:
            remaining_rows.append(row)

    return remaining_rows

