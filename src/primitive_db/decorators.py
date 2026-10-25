import time


def _keep_metadata(wrapper, func):
    """Сохранить имя и описание исходной функции без дополнительных импортов."""
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper


def handle_db_errors(func):
    """Показать понятное сообщение при ошибке операции базы данных."""

    def wrapper(*args, **kwargs):
        """Выполнить операцию и вернуть None при обработанной ошибке."""
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print("Ошибка: Файл данных не найден.")
        except KeyError as error:
            print(f"Ошибка: Таблица или столбец {error} не найден.")
        except ValueError as error:
            print(f"Ошибка валидации: {error}")
        return None

    return _keep_metadata(wrapper, func)


def confirm_action(action_name):
    """Создать декоратор, запрашивающий согласие перед опасным действием."""

    def decorator(func):
        """Добавить подтверждение к выбранной функции."""

        def wrapper(*args, **kwargs):
            """Выполнить функцию только после ответа y."""
            answer = input(f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: ')
            if answer.strip().lower() != "y":
                print("Операция отменена.")
                return None
            return func(*args, **kwargs)

        return _keep_metadata(wrapper, func)

    return decorator


def log_time(func):
    """Вывести время выполнения функции, измеренное монотонными часами."""

    def wrapper(*args, **kwargs):
        """Вызвать функцию и напечатать затраченное время."""
        start = time.monotonic()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.monotonic() - start
            print(f"Функция {func.__name__} выполнилась за {elapsed:.3f} секунд")

    return _keep_metadata(wrapper, func)


def create_cacher():
    """Создать независимый кэш результатов в замыкании."""
    cache = {}

    def cache_result(key, value_func):
        """Вычислить результат один раз для ключа, не запоминая ошибки."""
        if key in cache:
            print("Результат взят из кэша.")
            return cache[key]

        result = value_func()
        # Ошибки не запоминаем. Пустой список является корректным результатом.
        if result is not None:
            cache[key] = result
        return result

    return cache_result
