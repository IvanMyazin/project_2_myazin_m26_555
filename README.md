# Primitive DB

`Primitive DB` — учебная консольная база данных на Python. Программа позволяет
создавать таблицы и выполнять основные CRUD-операции с данными.

Информация о таблицах и их столбцах сохраняется в файле `db_meta.json`. Записи
каждой таблицы хранятся в отдельном JSON-файле в директории `data/`. Поэтому
таблицы и их данные остаются доступными после перезапуска программы.

## Установка

Для работы необходимы Python 3.12 или новее и пакетный менеджер `uv`.

Установите зависимости проекта:

```bash
uv sync
```

## Запуск

Запустите базу данных командой:

```bash
uv run database
```

После сборки пакет можно установить как консольный инструмент:

```bash
uv tool install --force dist/primitive_db-0.1.0-py3-none-any.whl
database
```

## Управление таблицами

Программа поддерживает следующие команды:

```text
create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> ...
list_tables
drop_table <имя_таблицы>
help
exit
```

Доступные типы данных:

- `int` — целое число;
- `str` — строка;
- `bool` — логическое значение.

При создании таблицы программа автоматически добавляет столбец `ID:int`.

## CRUD-операции

### Добавление записи

```text
insert into <имя_таблицы> values (<значение1>, <значение2>, ...)
```

Столбец `ID` указывать не нужно: программа создаёт его автоматически. Строковые
значения необходимо заключать в двойные кавычки.

Пример:

```text
insert into users values ("Sergei", 28, true)
```

### Чтение записей

Получить все записи:

```text
select from users
```

Получить записи по условию:

```text
select from users where age = 28
```

### Обновление записей

```text
update users set age = 29 where name = "Sergei"
```

### Удаление записей

```text
delete from users where ID = 1
```

### Информация о таблице

```text
info users
```

Команда показывает структуру таблицы и количество записей.

## Пример использования

```text
Введите команду: create_table users name:str age:int is_active:bool
Таблица "users" успешно создана со столбцами: ID:int, name:str, age:int, is_active:bool

Введите команду: insert into users values ("Sergei", 28, true)
Запись с ID=1 успешно добавлена в таблицу "users".

Введите команду: select from users
+----+--------+-----+-----------+
| ID |  name  | age | is_active |
+----+--------+-----+-----------+
| 1  | Sergei |  28 |    True   |
+----+--------+-----+-----------+

Введите команду: update users set age = 29 where name = "Sergei"
Обновлено записей: 1.

Введите команду: delete from users where ID = 1
Удалено записей: 1.

Введите команду: info users
Таблица: users
Столбцы: ID:int, name:str, age:int, is_active:bool
Количество записей: 0

Введите команду: exit
Выход из программы
```

## Демонстрация

[![asciinema: установка и CRUD-операции](https://asciinema.org/a/kOxqnBcM8hdMeDdX.svg)](https://asciinema.org/a/kOxqnBcM8hdMeDdX)

## Проверка кода

Проверить проект с помощью Ruff:

```bash
uv run ruff check .
```

Собрать пакет:

```bash
uv build
```

Проверить собранный пакет:

```bash
uvx twine check dist/*
```
