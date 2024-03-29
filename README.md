### Задание для Python разработчика

1. Распарсить Excel

2. Загрузить в базу данных PostGIS

3. Создать API:

4. Настроить Docker:

## Выполнение заданий

1. Парсинг Excel файла

Написать скрипт на Python для парсинга данных из Excel файла.

Скрипт находится в файле parsing_data.py

Запуск файла:

```
cd transport_data  
cd parsing  
$ python parsing_data.py
```

Добавлены декораторы для измерения времени выполнения функции.

2. Загрузка данных в базу данных PostGIS

- Создание таблицы в базе данных PostGIS для хранения данных из Excel.
- Написать скрипт для загрузки данных из Excel в созданную таблицу.

Скрипт находится в файле create_database.py

Запуск файла:

```
python create_database.py
```

3. Создание API:

- Написать веб-приложение с использованием Flask.
- Реализовать следующие эндпоинты:

  - /vehicles:
    GET запрос для получения всех машин с последней геометрией.

  - /vehicles/{vehicle_id}:
    GET запрос для получения конкретной машины с последней геометрией.

  - /vehicles/{vehicle_id}/track:
    GET запрос для построения трека по дате или временному диапазону для конкретной машины.

- Использовать flask для создания API.

Для запуска Flask api:

```  
python manage.py
```

4. Настройка Docker:

- Создать Dockerfile для сборки Docker-образа.
- Убедиться, что в Dockerfile прописаны все необходимые шаги для создания окружения, установки зависимостей и запуска приложения.
- Учесть возможные переменные окружения и их передачу в контейнер.

Для сборки Docker образа:

```  
docker build -t test_task .
```

Для запуска контейнера:

```  
docker run -d -p 5473:80 test_task
```
