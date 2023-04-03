### Получение и создание подписок через API

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/nikitka133/api_final_yatube
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

## Примеры запросов:
#### Подписаться на автора:
http://localhost:8000/api/v1/follow/
###### Тело POST запроса:
```
{
    "following": "Username автора"
}
```

#### Получение всех подписок:
http://localhost:8000/api/v1/follow/

#### Технологии:
##### Django
##### Django rest framework

## Авторы: 
#### https://github.com/nikitka133/
#### https://github.com/yandex-praktikum/