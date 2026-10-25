#!/usr/bin/env python3
from .engine import run


def main() -> None:
    """Запустить консольный интерфейс базы данных."""
    print("DB project is running!")
    run()


if __name__ == "__main__":
    main()
