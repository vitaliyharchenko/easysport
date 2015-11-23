# sportcourts2

Initial commit

Инструкция по развертыванию проекта для локальной разработки:

1) установка PyCharm

2) 
```
git clone https://github.com/vitaliyharchenko/sportcourts2.git
```

3) открыть как проект в PyCharm

4) создание virtualenv вне папки проекта. Pycharm-Preferences-Project-Interpreter-create virtualenv

5) В virtualenv 

```
install django
```

6)
```
psql
CREATE USER scuser WITH PASSWORD '123456';
CREATE DATABASE scdb OWNER scuser;
ALTER USER scuser CREATEDB;
\q
```

10) install psycopg2

```
cd scenv (ссылка к виртуальному окружению)
source bin/activate
pip install psycopg2
cd sportcourts (путь к проекту)
python manage.py makemigrations
python manage.py migrate
python manage.py syncdb
create user - admin, ceo@sportcourts.ru, 123456
```

11) set database in PyCharm
