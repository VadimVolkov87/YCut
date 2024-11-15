# Приложение для укорачивания ссылок YaCut

Репозиторий `yacut` содержит приложение для создания и хранения коротких ссылок связанных с оригинальными, обычными ссылками пользователей. Пользователь имеет возможность как придумать короткую ссылку сам, так и получить сгенерированную приложением ссылку. Ссылки нужно ввести в форму на главной странице и нажать клавишу "Создать". В состав приложения входят модули для пользовательского приложения и API.

## Стек приложения

Приложение создано на основе:

* Python
* Flask
* SQLAlchemy
* WTForms
* Jinja2

## Для запуска проекта необходимо

Клонировать репозиторий:

```bash
git clone https://github.com/VadimVolkov87/yacut
```

Перейти в корневую папку приложения:

```bash
cd yacut
```

Создать и активировать виртуальное окружение:

```bash
python -m venv venv
```

```bash
source venv/Scripts/activate
```

Установить пакеты из файла зависимостей:

```bash
pip install -r requirements.txt
```

Создать миграции:

```bash
flask db migrate -m "Create db"
```

Применить миграции(создать базу данных):

```bash
flask db upgrade
```

Запустить сервер командой терминала из корневой директории проекта:

```bash
flask run
```

## Автор проекта

Вадим Волков - разработка

[Вадим Волков](https://github.com/VadimVolkov87/)
[Flask API](https://flask.palletsprojects.com/en/stable/api/#)
