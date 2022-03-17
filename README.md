# README #

How to install:
* create database and user with followed commands
```
    sudo -u postgres createdb -U postgres -E UTF8 -T template0 --locale=ru_RU.UTF-8 "luggage"
    sudo -u postgres psql -c "create user \"luggage\" with password 'luggage';"
    sudo -u postgres psql -c "grant all on database \"luggage\" to \"luggage\";"
    sudo -u postgres psql -d luggage  -c "CREATE EXTENSION postgis;"
```
* create virtual env
```
virtualenv2 venv
```
* install required packages
```
./venv/bin/pip install -r requirments.txt
```
* Create tables
```
./venv/bin/python manage.py migrate
```
* Copy default local settings and set proper values
```
cp ./project/settings_local_example.py ./project/settings_local.py
vim ./project/settings_local.py
```
* Sync customers with Stripe
```
./venv/bin/python ./manage.py init_customers
```
* Load geodateabse
```
./venv/bin/python ./manage.py cities
```
* Load change rate
```
./manage.py currencies --import=USD --import=MXN
./manage.py updatecurrencies

```
* Configure crontab
```
* * * * * chuda (cd /var/www/luggage && venv/bin/python manage.py send_queued_mail >> venv/send_mail.log 2>&1)
00 23 * * * chuda (cd /var/www/luggage && venv/bin/python manage.py updatecurrencies >> venv/update_currency.log 2>&1)
00 10 * * * chuda (cd /var/www/luggage && venv/bin/python manage.py send_remind_email >> venv/send_remind.log 2>&1)

```
* Configure and run your webserver as usual
