### Описание
Реализован сервис, который позволяет динамически управлять конфигурацией приложений.
- сервис обеспечивает "частичную" персистентность данных (хранятся все версии, но изменять и удалять можно только последнюю)
- сервис поддерживает все CRUD операции по работе с конфигурациями
- поддерживается версионирование конфигурации при его изменении (у каждой версии есть метка времени)
- удалить конфигурацию приложения возможно только если нет других версий, иначе удаляется последняя версия

### Технологии
```
Django
Django Rest Framework
Docker
```

### Demo:


### Как запустить проект:
Клонировать проект
```
git clone https://github.com/robky/cloudtask.git
```

Из папки deploy запустить контейнеры и выполнить команды
```
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --no-input
```


