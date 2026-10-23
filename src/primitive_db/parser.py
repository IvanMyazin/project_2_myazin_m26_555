def parse_value(value):
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
    if "=" not in condition:
        raise ValueError("В условии отсутствует знак =.")

    column, value = condition.split("=", 1)
    column = column.strip()
    value = value.strip()

    if not column or not value:
        raise ValueError("Условие заполнено неправильно.")

    return {column: parse_value(value)}


def parse_where_clause(condition):
    return parse_condition(condition)


def parse_set_clause(condition):
    return parse_condition(condition)


def parse_values(values_text):
    values_text = values_text.strip()

    if not values_text.startswith("(") or not values_text.endswith(")"):
        raise ValueError("Значения должны находиться в круглых скобках.")

    values_text = values_text[1:-1]
    values = []

    for value in values_text.split(","):
        values.append(parse_value(value))

    return values
