def parse_value(value):
    """Преобразовать текст в int, bool или строку в двойных кавычках."""
    value = value.strip()

    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]

    if value.lower() == "true":
        return True

    if value.lower() == "false":
        return False

    try:
        return int(value)
    except ValueError:
        raise ValueError("Строковое значение должно быть в кавычках.") from None


def parse_condition(condition):
    """Разобрать одно условие вида age = 28 в словарь."""
    if "=" not in condition:
        raise ValueError("В условии отсутствует знак =.")

    column, value = condition.split("=", 1)
    column = column.strip()
    value = value.strip()

    if not column or not value:
        raise ValueError("Условие заполнено неправильно.")

    return {column: parse_value(value)}


def parse_where_clause(condition):
    """Разобрать условие поиска записей."""
    return parse_condition(condition)


def parse_set_clause(condition):
    """Разобрать столбец и новое значение для обновления."""
    return parse_condition(condition)


def parse_values(values_text):
    """Разобрать список значений в круглых скобках для insert."""
    values_text = values_text.strip()

    if not values_text.startswith("(") or not values_text.endswith(")"):
        raise ValueError("Значения должны находиться в круглых скобках.")

    values_text = values_text[1:-1]
    values = []

    for value in values_text.split(","):
        values.append(parse_value(value))

    return values
