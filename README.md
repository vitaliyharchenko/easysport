# Easysport v1.0


## Резервное копирование
```
python manage.py dumpdata > db.json
```


## Поднимаем сервер

```
Установка Ubuntu ubuntu14.04-x86_64
ssh-keygen -R 194.58.108.127
ssh root@194.58.108.127

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

uwsgi --ini sportcourts_uwsgi.ini
uwsgi --stop sportcourts_uwsgi.ini

nano /etc/init/uwsgi.conf

description "uwsgi tiny instance"
start on runlevel [2345]
stop on runlevel [06]
respawn
exec uwsgi --ini /opt/sportcourts2/sportcourts_uwsgi.ini
```
