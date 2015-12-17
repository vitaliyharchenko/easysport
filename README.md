# sportcourts2

Initial commit

# Инструкция по развертыванию проекта для локальной разработки:

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
CREATE USER scuser WITH PASSWORD '4203';
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

# обнуление БД

'''
sudo su postgres -c 'pg_ctl -D /opt/local/var/db/postgresql84/defaultdb/ restart' (рестарт psql)
psql
DROP DATABASE scdb;
CREATE DATABASE scdb OWNER scuser;
ALTER USER scuser CREATEDB;
python manage.py makemigrations api users courts games places sports users
python manage.py migrate
python manage.py createsuperuser
create user - admin, ceo@sportcourts.ru, 123456
'''


# Работа с зависимостями
'''
pip install -r requirements.txt
pip freeze > requirements.txt

npm update --save
npm outdated
'''

# Работа с удаленкой #
```
lt --port 8000
```

# Развертываем фронтенд #
'''
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

bower init

git config http.sslVerify false
bower install bootstrap-sass --save
bower install jquery-ui --save
bower install fontawesome --save
bower install social-likes --save
bower install jasny-bootstrap --save
bower install jasny-bootstrap --save

далее gulp в директории проекта
'''


# Деплой на сервер

Подключение к серверу
'''
    Установка Ubuntu ubuntu14.04-x86_64
    ssh-keygen -R 194.58.108.127
    ssh root@194.58.108.127
    OKBxmNX*GL6rg1
'''

    
Установка зависимостей на Ubuntu    
'''    
    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install libpq-dev python3.4-dev libjpeg8 libjpeg62-dev
    sudo apt-get install libfreetype6 libfreetype6-dev
    sudo apt-get build-dep python-imaging
    sudo apt-get install python-virtualenv git nginx postgresql postgresql-contrib
    apt-get install python3-pip
'''

Устанавливаем базу данных
'''
    sudo su - postgres
    psql
    create user "scuser" with password '4203';
    create database "scdb" owner "scuser";
    alter user scuser createdb;
    grant all privileges on database scdb TO scuser;
    \q
    su - root
'''


Поднимаем виртуальное окружение
'''
    sudo virtualenv /opt/scenv --python=python3.4
    source /opt/scenv/bin/activate
    cd /opt
    git clone https://github.com/vitaliyharchenko/sportcourts2.git
    pip install -r /opt/sportcourts2/requirements.txt
    pip install uwsgi
'''

Test Django-uwsgi
'''
    cd /opt/sportcourts2
    python manage.py collectstatic
    python manage.py makemigrations api courts games places sports users notifications
    python manage.py migrate
    python manage.py createsuperuser
    create user - admin, ceo@sportcourts.ru, 123456
    
    python manage.py runserver 0.0.0.0:8000
    go to http://test.sportcourts.ru:8000
    
    uwsgi --http :8000 --module sportcourts.wsgi
    go to http://test.sportcourts.ru:8000
    the web client <-> uWSGI <-> Django | works
    
    go to http://test.sportcourts.ru
    the web client <-> the web server |works
'''

Set up nginx
'''
sudo nano /etc/nginx/sites-available/sportcourts
'''

'''
# mysite_nginx.conf

# the upstream component nginx needs to connect to
upstream django {
    # server unix:///opt/sportcourts2/sportcourts.sock; # for a file socket
    server 127.0.0.1:8001; # for a web port socket (we'll use this first)
}

# configuration of the server
server {
    # the port your site will be served on
    listen      8000;
    # the domain name it will serve for
    server_name test.sportcourts.ru; # substitute your machine's IP address or FQDN
    charset     utf-8;

    # max upload size
    client_max_body_size 75M;   # adjust to taste

    # Django media
    location /media  {
        alias /opt/sportcourts2/media;  # your Django project's media files - amend as required
    }

    location /static {
        alias /opt/sportcourts2/static; # your Django project's static files - amend as required
    }

    # Finally, send all non-media requests to the Django server.
    location / {
        uwsgi_pass  django;
        include     /opt/sportcourts2/uwsgi_params; # the uwsgi_params file you installed
    }
}
'''

'''
cd /etc/nginx/sites-enabled
sudo ln -s ../sites-available/sportcourts
sudo rm default
sudo service nginx restart

go to http://test.sportcourts.ru:8000/static/css/main.css
Nginx serving static and media correctly

uwsgi --socket :8001 --wsgi-file test.py
go to http://test.sportcourts.ru:8000
the web client <-> the web server <-> the socket <-> uWSGI <-> Python | works correctly

sudo nano /etc/nginx/sites-available/sportcourts
uncomment # server unix:///opt/sportcourts2/sportcourts.sock; # for a file socket
sudo service nginx restart

uwsgi --socket sportcourts.sock --wsgi-file test.py --chmod-socket=666
go to http://test.sportcourts.ru:8000
socket works correctly

uwsgi --socket sportcourts.sock --module sportcourts.wsgi --chmod-socket=666
'''

Install uWSGI system-wide
'''
deactivate
sudo pip3 install uwsgi
'''

простой старт сервера
'''
uwsgi --ini sportcourts_uwsgi.ini
'''

Emperor mode for uwsgi
'''
# create a directory for the vassals
sudo mkdir /etc/uwsgi
sudo mkdir /etc/uwsgi/vassals
# symlink from the default config directory to your config file
sudo ln -s /opt/sportcourts2/sportcourts_uwsgi.ini /etc/uwsgi/vassals/
# run the emperor
uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data
'''


    
cd /etc/nginx/sites-enabled
sudo ln -s ../sites-available/sportcourts
sudo rm default
sudo service nginx restart

source /opt/scenv/bin/activate
locale-gen ru_RU.UTF-8

cd /opt/sportcourts2
python manage.py runserver 0.0.0.0:8000
uwsgi --http :8000 --module sportcourts.wsgi
python manage.py collectstatic
python manage.py makemigrations api courts games places sports users notifications
python manage.py migrate
python manage.py migrate --fake
python manage.py createsuperuser
create user - admin, ceo@sportcourts.ru, 123456


python manage.py makemigrations
python manage.py migrate
python manage.py syncdb
create user - admin, ceo@sportcourts.ru, 123456
pip install gunicorn
cd /opt/scenv
sudo nano gunicorn_config.py

    command = '/opt/myenv/bin/gunicorn'
    pythonpath = '/opt/myenv/myproject'
    bind = '127.0.0.1:8001'
    workers = 3

'''

