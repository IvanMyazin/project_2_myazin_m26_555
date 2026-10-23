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


