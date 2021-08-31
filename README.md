# Payment Service

This is test API app

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.
Documentation available at [documenter.getpostman.com](https://documenter.getpostman.com/view/13009350/U16bx9Mu), you can read about Payment Service.

### Prerequisites

What things you need to install the software and how to install them

```
Docker v20.10.2 or newer
```

### Installing

Clone repository to your pc and build docker image, run from the app directory

```
docker build -t payment_service .
```

Then you need to run container

```
docker run -it -p 8000:8000 payment_service
```

Now container is running on localhost:8000. Now yo need go into container, run

```
docker ps
docker exec -it <CONTAINER ID> bash
```

You need to make migrations

```
python manage.py makemigrations
python manage.py migrate
```

and create superuser

```
python manage.py createsuperuser
```


## Project avalible at

[Redoc](http://130.193.52.84/redoc/) - This is redoc page, you can read about YaMDB_API
[Admin](http://localhost:8000/admin/) - This is admin login page
[API](http://localhost:8000/api/v1/auth/users/) - You can create regular user and check API


## Built With

* [Django 3.2.6](https://docs.djangoproject.com/en/3.2/) - The web framework used
* [Django REST framework 3.12.4](https://www.django-rest-framework.org/) - The REST framework used
* [SQLite](https://www.sqlite.org/index.html) - Object-relational database system used
* [Docker 20.10.8](https://www.docker.com/) - Package software used
* [JWT 2.1.0](https://jwt.io//) - JSON Web Token
* [djoser 2.1.0](https://djoser.readthedocs.io/en/latest/getting_started.html) - Django authentication system


## Authors

* **Fedor Mityanin** - [Fyodor-Mityanin](https://github.com/Fyodor-Mityanin)
