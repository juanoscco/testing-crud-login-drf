# testing-crud-login-drf
Creation of an application in django on music albums

## Before
Before you must verify that you have the latest python version downloaded

# Start
In your terminal
first create a virtual environment
```sh
python -m venv env
```
In windows
```sh
env\Scripts\activate.bat
```
In Unix o MacOS run
```sh
source env\Scripts\activate.bat
```
Run the command
```sh
pip install -r requirements.txt
```

Create an .env file in the same location as the manage.py file

### inside the .env file
```sh
  - DJANGO_SETTINGS_MODULE = 'app.settings'
  - DB_ENGINE = 'django.db.backends.postgresql'
  - DB_NAME = DATABASE NAME
  - DB_USER = NAME USER IN THE DATABASE
  - DB_PASSWORD = DATABASE PASSWORD
  - DB_HOST = '127.0.0.1'
  - DB_PORT = '5432'
```

## After
Run the command to perform the migrations to the database
```sh
  python manage.py makemigrations core
```
then run the command

```sh
  python manage.py migrate
```
and then run the command
```sh
  python manage.py runserver
```


### This is the page
[![Captura.png](https://i.postimg.cc/PJnsfL7T/Captura.png)](https://postimg.cc/KkfsJYFH)

# Sign in, Sign up and authentication token
Get started by creating an account

[![1.png](https://i.postimg.cc/WbVPZ7Xs/1.png)](https://postimg.cc/G9XNwGWf)

[![2.png](https://i.postimg.cc/jdhY4JFP/2.png)](https://postimg.cc/QHVzXVsd)

Then login with login

[![3.png](https://i.postimg.cc/XYHXNv9S/3.png)](https://postimg.cc/PCDd2T62)

![4](https://user-images.githubusercontent.com/58866695/148983878-8338d2a9-bf39-4bac-b243-ed6533e0ec23.PNG)

Then authenticate

![5](https://user-images.githubusercontent.com/58866695/148984055-155c937c-f706-4595-9211-de279ab1289a.PNG)

