### Описание
Реализован сервис, который позволяет динамически управлять конфигурацией приложений.
- сервис обеспечивает "частичную" персистентность данных (хранятся все версии, но изменять и удалять можно только последнюю)
- сервис поддерживает все CRUD операции по работе с конфигурациями
- поддерживается версионирование конфигурации при его изменении (у каждой версии есть метка времени)
- удалить конфигурацию приложения возможно только если нет других версий, иначе удаляется последняя версия

Для проверки сервиса написаны тесты.
Созданы спецификации Swagger/ReDoc/OpenAPI 2.0 из API Django Rest Framework при помощи drf-yasg.

![branch parameter](https://github.com/robky/cloudtask/actions/workflows/tests.yml/badge.svg)

### Технологии
```
Django
Django Rest Framework
SQLite
drf-yasg
Docker
```

### Demo (тестовый пример):

https://cloudtask.cvdev.ru/


### Как запустить проект:
Клонировать проект
```
git clone https://github.com/robky/cloudtask.git
```

Перейти в папку deploy и выполнить команды:
```
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --no-input
```


