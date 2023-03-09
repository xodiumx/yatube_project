# Yatube
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)

# Description
### Мой первый учебный проект, мини соц. сеть yatube 👀
У вас есть возможность зарегистрироваться и вести собственный блог, создавать посты, загружать картинки, ставить лайки и многое другое.

# Available features
### Функционал:

- Создание постов (редактирование и удаление)
- Просмотр своего профиля
- Возможность подписаться на понравившихся авторов (отписаться)
- Возможность отслеживать своих подписчиков (подписки)
- Просмотр ленты подписок
- Ставить лайки публикациям других авторов
- Комментировать публикации
- другие.

# Technology

- Python 3.7
- Django 2.2.19
- Bootstrap
- little bit jQuery with ajax
- другие.

# Как развернуть проект
- Клонируйте данный репозиторий на свой компьютер
```
git clone https://github.com/xodiumx/yatube_project
```
- Cоздать и активировать виртуальное окружение:
```
py -3.10 -m venv venv
```
- Активировать venv
```
source venv/Scripts/activate или source env/bin/activate для mac
```
- Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
- Выполнить миграции:
```
python manage.py makemigrations
```
```
python manage.py migrate
```
- Запустить проект из директории где находится файл manage.py:
```
python manage.py runserver
```

# Try it [project](http://alekseev.pythonanywhere.com/)
# Author - [Alekseev Maksim](https://t.me/maxalxeev)
