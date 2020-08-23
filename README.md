# Find out your rubbish collection day
This is an app in which you can find out when your rubbish will be collected.

I did it for my city - Wołomin. You can check how it works on [my website](https://kalendarz.pyapp.pl/?utm_source=GitHub&utm_medium=readme).

---

## Features
* easy searching
* readable format
* ical files
* responsive version for mobiles

![alt text](https://kalendarz.pyapp.pl/static/schedule/img/header-img.png "Screen from app")

---

## Technologies
* Python 3.7
* Django 3.1
* PostgreSQL 12
* pytest
* Docker

---

## Setup
Clone project:
```bash
git clone git@github.com:efefre/rubbish_collection_day_2.git
```
Use:
* [Docker](https://docs.docker.com/install/)
* [docker-compose](https://docs.docker.com/compose/install/)

Run project:
```bash
make start
```

Makemigrations:
```bash
make makemigrations
```

Migrate:
```bash
make migrate
```

Create super user (root):
```bash
make createsuperuser
```

Open:
```bash
127.0.0.1:8000
```

_More details about [make](https://github.com/efefre/rubbish_collection_day_2/blob/master/Makefile)_.

---

## Status
Project is: _in progress_.

