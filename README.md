# API-сервис для онлайн-кинотеатра

Основной репозиторий находится [тут](https://github.com/mikhail349ya/Async_API_sprint_1)

В качестве ETL проекта используется [данный репозиторий](https://github.com/mikhail349ya/new_admin_panel_sprint_3)

## Первый запуск

1. Сформировать виртуальное Python-окружение `python -m venv venv`
2. Установить зависимости `pip install -r requirements`
3. Создать файл `.env` с переменными окружения по аналогии с файлом `.env.example`
3. Запустить докер `docker-compose up --build`

## Линтер

Запуск: в корне проекта `flake8`

## Тестирование

1. Перейти в папку с фунциональными тестами `cd tests/functional`
2. Сформировать виртуальное Python-окружение `python -m venv venv`
3. Установить зависимости `pip install -r requirements`
4. Создать файл `.env` с переменными окружения по аналогии с файлом `.env.example`
5. Запустить докер `docker-compose up --build`