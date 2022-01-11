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
![Captura](https://user-images.githubusercontent.com/58866695/148984889-830df87e-2aad-4e4c-b2b7-73c56aa59844.PNG)


# Sign in, Sign up and authentication token
Get started by creating an account

![1](https://user-images.githubusercontent.com/58866695/148984917-87763db7-2da3-43ee-8f31-2aa64a252218.PNG)

![2](https://user-images.githubusercontent.com/58866695/148984936-fb499fed-ad5f-4914-a18d-d9d2c7bf02cf.PNG)


Then login with login
![3](https://user-images.githubusercontent.com/58866695/148984974-a426deb0-2189-4db4-b689-7f7d62fada3d.PNG)


![4](https://user-images.githubusercontent.com/58866695/148983878-8338d2a9-bf39-4bac-b243-ed6533e0ec23.PNG)

Then authenticate

![5](https://user-images.githubusercontent.com/58866695/148984055-155c937c-f706-4595-9211-de279ab1289a.PNG)

# Add artist, gender, songs and album

Add gender

![6](https://user-images.githubusercontent.com/58866695/148985143-ad5bc27c-2d6f-42f6-8c5a-748f53af6512.PNG).

Get gender

![7](https://user-images.githubusercontent.com/58866695/148985230-af358f3b-5750-4788-8ff9-0bca088b51fa.PNG)

Add artist

![8](https://user-images.githubusercontent.com/58866695/148985375-a463a6d2-08ee-417b-a0a2-6585238e3e1e.PNG)

Get artist
![9](https://user-images.githubusercontent.com/58866695/148985393-804a4cce-408b-4f32-b4f1-41192f859cf7.PNG)

Add song

![10](https://user-images.githubusercontent.com/58866695/148985472-27c455c5-2b5a-4f60-a4ec-89ad906c8109.PNG)

Get song

![11](https://user-images.githubusercontent.com/58866695/148985513-679f635b-8758-4aa5-af61-98080bb31c86.PNG)

Add album

![12](https://user-images.githubusercontent.com/58866695/148985569-ebf46796-940d-4b20-a1fb-78293de9f40d.PNG)

Get album

![13](https://user-images.githubusercontent.com/58866695/148985609-4cecdced-dd70-4d9c-a54a-31f19cb270c6.PNG)
![14](https://user-images.githubusercontent.com/58866695/148985628-021aeb67-ce2f-4ebc-a75c-0eb5fae43e52.PNG)


# Logout

It is very important to log out
you only need to do this.

![15](https://user-images.githubusercontent.com/58866695/148986009-795388ae-6f2e-4b65-b26f-9c3340f3d87e.PNG)

then press logout
![16](https://user-images.githubusercontent.com/58866695/148986193-503be5d3-7810-49da-9c86-1a1cd5c1ef77.PNG)




