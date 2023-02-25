## Contents

- [Team](#team)
- [Personal-Spending-Tracker](#personal-spending-tracker)
- [Project structure](#project-structure)
- [Deployed version of the application](#deployed-version-of-the-application)
- [Installation instructions](#installation-instructions)
- [References](#references)

## Team

- Haris Malik
- Joel Jolly
- Konrad Bylina
- Malika Boss
- Oreoluwa Fayemiwo
- Richmond Bobie
- Vanessa Neboh

## Personal-Spending-Tracker

Track your daily spending, create, edit delete categories, create streaks by reaching your targets and compare your achievements with friends

## Project structure

The project is called personal-spending-tracker. It currently consists of a single app expenditure where all functionality resides.

## Deployed version of the application

The deployed version of the application can be found at \_\_\_

## Installation instructions

To install the software and use it in your local development environment, you must first set up and activate a local development environment. From the root of the project:

```
$ virtualenv venv
$ source venv/bin/activate
```

Install all required packages:

```
$ pip3 install -r requirements.txt
```

Get key for API:

```
- visit https://newsapi.org/
- Sign up to obtain a key
- Create a file in your root folder(usually where manage.py is located) and name it '.env'
- In your .env file, type: NEWS_API_KEY = add your key here(no quotes)
```

Migrate the database:

```
$ python3 manage.py makemigrations
```

```
$ python3 manage.py migrate
```

Seed the development database with:

```
$ python3 manage.py seed
```

Run all tests with:

```
$ python3 manage.py test
```

Run server:

```
Note: Before running server, check apps.py file and uncomment the code below to start scheduler
- scheduler.start()
```

```
$ python3 manage.py runserver
```

## References

CODE

- https://www.w3schools.com/howto/howto_js_treeview.asp
- https://django-betterforms.readthedocs.io/en/latest/multiform.html#working-with-createview
- https://www.chartjs.org/docs/latest/

IMAGES
https://pixabay.com/illustrations/pound-uk-money-currency-finance-685059/

TEMPLATES

OTHER
