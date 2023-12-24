# Julbl

Julbl представляет из себя ресурс, который соберет в себя различную информацию 
по теме физического и ментального здоровья. Сейчас это крайне актуальный вопрос 
как среди молодого поколения, так и более взрослого.

## библиотеки

`django - 3.2.14`

`pillow - 10.1.0`

## установка

```bash
# скачивание проекта
git clone git@github.com:Julbl/store-site.git

# установка библиотек
pip install -r requirements.txt

# подготовка
python manage.py makemigrations
python manage.py migrate --run-syncdb
python manage.py createsuperuser
```

## запуск

```bash
python manage.py runserver
```
