# sportcourts v2.0

# На локальной машине:

```
git clone https://github.com/vitaliyharchenko/sportcourts2.git
create venv
source venv/bin/activate
pip install -r requirements.txt
psql
CREATE USER scuser WITH PASSWORD '$$$$';
CREATE DATABASE scdb OWNER scuser;
ALTER USER scuser CREATEDB;
\q
pip install psycopg2
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

# обнуление БД

```
sudo su postgres -c 'pg_ctl -D /opt/local/var/db/postgresql84/defaultdb/ restart' (рестарт psql)
psql
DROP DATABASE scdb;
CREATE DATABASE scdb OWNER scuser;
ALTER USER scuser CREATEDB;
python manage.py makemigrations api users courts games places sports users
python manage.py migrate
python manage.py createsuperuser
create user - admin, ceo@sportcourts.ru, 123456
```


# Работа с зависимостями
```
pip install -r requirements.txt
pip freeze > requirements.txt
npm update --save
npm outdated
```

# Резервное копирование #
```
python manage.py dumpdata > db.json
```

# Развертываем фронтенд #
```
npm install --save-dev gulp - в директории проекта
npm init

npm i gulp-autoprefixer --save
npm i gulp-minify-css --save
npm i gulp-imagemin --save
npm i imagemin-pngquant --save
npm i gulp-uglify --save
npm i rimraf --save
npm i gulp-sass --save
npm i gulp-sourcemaps --save
npm i gulp-rigger --save
npm i gulp-watch --save
npm i gulp-jade --save
npm i gulp-inline --save


bower init

git config http.sslVerify false
bower install bootstrap-sass --save
bower install jquery-ui --save
bower install fontawesome --save
bower install social-likes --save
bower install jasny-bootstrap --save
bower install jasny-bootstrap --save

далее gulp в директории проекта
```

# Миграция старой БД

```
python users_delete.py
python filldb.py
python manage.py loaddata users_all.xml
python users_render.py
```


# Поднимаем сервер
```
Установка Ubuntu ubuntu14.04-x86_64
ssh-keygen -R 194.58.108.127
ssh root@194.58.108.127
OKBxmNX*GL6rg1
sudo apt-get update
sudo apt-get upgrade
apt-get install python3-pip
sudo apt-get install libpq-dev python3.4-dev libjpeg8 libjpeg62-dev
sudo apt-get install libfreetype6 libfreetype6-dev
sudo apt-get build-dep python-imaging
sudo apt-get install python-virtualenv git nginx postgresql postgresql-contrib
locale-gen ru_RU.UTF-8

sudo su - postgres
psql
create user "scuser" with password '4203';
create database "scdb" owner "scuser";
alter user scuser createdb;
grant all privileges on database scdb TO scuser;
\q
su - root

sudo virtualenv /opt/scenv --python=python3.4
source /opt/scenv/bin/activate
cd /opt
git clone https://github.com/vitaliyharchenko/sportcourts2.git
pip install -r /opt/sportcourts2/requirements.txt
pip install uwsgi
```

# Test Django-uwsgi
```
cd /opt/sportcourts2
python manage.py collectstatic
python manage.py makemigrations api courts games places sports users notifications
python manage.py migrate
python manage.py createsuperuser
create user - admin, ceo@sportcourts.ru, 123456
python manage.py runserver 0.0.0.0:8000
go to http://sportcourts.ru:8000
uwsgi --http :8000 --module sportcourts.wsgi
go to http://sportcourts.ru:8000
the web client <-> uWSGI <-> Django | works
go to http://sportcourts.ru
the web client <-> the web server |works
```


# Set up nginx
```
sudo nano /etc/nginx/sites-available/sportcourts
look at sportcourts.conf file
cd /etc/nginx/sites-enabled
sudo ln -s ../sites-available/sportcourts
sudo rm default
sudo service nginx restart

go to http://sportcourts.ru:8000/static/css/main.css
Nginx serving static and media correctly

uwsgi --socket :8001 --wsgi-file test.py
go to http://sportcourts.ru:8000
the web client <-> the web server <-> the socket <-> uWSGI <-> Python | works correctly

sudo nano /etc/nginx/sites-available/sportcourts
uncomment # server unix:///opt/sportcourts2/sportcourts.sock; # for a file socket
sudo service nginx restart

uwsgi --socket sportcourts.sock --wsgi-file test.py --chmod-socket=666
go to http://sportcourts.ru:8000
socket works correctly

uwsgi --socket sportcourts.sock --module sportcourts.wsgi --chmod-socket=666

Install uWSGI system-wide

deactivate
sudo pip3 install uwsgi
```

# старт сервера
```
uwsgi --ini sportcourts_uwsgi.ini
uwsgi --stop sportcourts_uwsgi.ini
```

# автоматический старт сервера после перезагрузки
```
nano /etc/init/uwsgi.conf

description "uwsgi tiny instance"
start on runlevel [2345]
stop on runlevel [06]
respawn
exec uwsgi --ini /opt/sportcourts2/sportcourts_uwsgi.ini
```
