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

# обнуление БД

'''
psql
DROP DATABASE scdb;
CREATE DATABASE scdb OWNER scuser;
ALTER USER scuser CREATEDB;
python manage.py makemigrations users
python manage.py migrate users
python manage.py syncdb
create user - admin, ceo@sportcourts.ru, 123456
'''


# Работа с зависимостями
'''
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

bower install bootstrap-sass --save
bower install jquery-ui --save
bower install fontawesome --save
bower install social-likes --save

далее gulp в директории проекта
'''


# Деплой на сервер

'''
Установка Ubuntu ubuntu14.04-x86_64
ssh root@194.58.108.127
OKBxmNX*GL6rg1
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python-virtualenv
sudo apt-get install git
sudo apt-get install nginx
sudo apt-get build-dep python-imaging
sudo apt-get install libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev
sudo virtualenv /opt/scenv
sudo apt-get install git
source /opt/scenv/bin/activate
pip install django
deactivate
sudo apt-get install libpq-dev python-dev
sudo apt-get install postgresql postgresql-contrib
sudo su - postgres
psql
create user "scuser" with password '4203';
create database "scdb" owner "scuser";
alter user scuser createdb;
grant all privileges on database scdb TO scuser;
\q
su - root
source /opt/scenv/bin/activate
pip install psycopg2
git clone https://github.com/vitaliyharchenko/sportcourts2.git
pip install -r /opt/sportcourts2/requirements.txt
cd /opt/sportcourts2
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
    
sudo nano /etc/nginx/sites-available/sportcourts

    server {
        server_name test.sportcourts.ru;
        charset utf-8;
        client_max_body_size 75M;  

        access_log off;

        location /static/ {
            alias /opt/scenv/static/;
        }

        location / {
                proxy_pass http://127.0.0.1:8001;
                proxy_set_header X-Forwarded-Host $server_name;
                proxy_set_header X-Real-IP $remote_addr;
                add_header P3P 'CP="ALL DSP COR PSAa PSDa OUR NOR ONL UNI COM N$
        }
    }
    
cd /etc/nginx/sites-enabled
sudo ln -s ../sites-available/sportcourts
sudo rm default
sudo service nginx restart
'''

