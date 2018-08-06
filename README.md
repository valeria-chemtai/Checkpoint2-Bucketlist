[![Build Status](https://travis-ci.org/valeria-chemtai/Checkpoint2-Bucketlist.svg?branch=master)](https://travis-ci.org/valeria-chemtai/Checkpoint2-Bucketlist)
[![Coverage Status](https://coveralls.io/repos/github/valeria-chemtai/Checkpoint2-Bucketlist/badge.svg?branch=master)](https://coveralls.io/github/valeria-chemtai/Checkpoint2-Bucketlist?branch=master)
# Bucketlist API
According to Merriam-Webster Dictionary,  a Bucket List is a list of things that one has not done before but wants to do before dying.

Bucketlist API is an online flask API built to help users keep track of their things to do

## Installation and Setup
Clone the repo
```
https://github.com/valeria-chemtai/Checkpoint2-Bucketlist.git
```
Navigate to the root folder
```
cd checkpoint2-Bucketlist
```
create a virtualenv using virtualenvwrapper
```
mkvirtualenv bucketlist
```
activate virtualenv by running the following
```
workon bucketlist
```
Inside virtualenv open a postactivate file to store a script for exporting `App_setting`, `secret key` and `database url` variables by running the command
```
subl $VIRTUAL_ENV/bin/postactivate
```
In the postactivate file add the following and replace the parenthesis in database_url with appropriate database owner name
```
export SECRET='akjshdkqiu3ye723y42i34'
export DATABASE_URL="postgres://{}@localhost:5432/bucketlist"
export FLASK_ENV="development"
```
Alternatively if you do not want to automate the export of variables using postactivate, a simple export on the command line before running the app will work as follows:
```
$ export SECRET='akjshdkqiu3ye723y42i34'
$ export DATABASE_URL="postgres://{}@localhost:5432/bucketlist"
$ export FLASK_ENV="development"
```

Install the requirements
```
pip install -r requirements.txt
```
Create a postgres database called bucketlist using PgAdmin, why? its easy

Alternatively create the database from the command line by running the script:
```
$ createdb bucketlist
```

Initialize, migrate, upgrade the datatbase
```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```
## Launch the progam
Run 
```
python manage.py runserver
```
Interact with the API, send http requests using Postman
## API Endpoints
| URL Endpoint | HTTP Methods | Summary |
| -------- | ------------- | --------- |
| `/auth/register/` | `POST`  | Register a new user|
|  `/auth/login/` | `POST` | Login and retrieve token|
| `/bucketlists/` | `POST` | Create a new Bucketlist |
| `/bucketlists/` | `GET` | Retrieve all bucketlists for user |
| `/bucketlists/?page=1&limit=3/` | `GET` | Retrieve three bucketlists per page |
 `/bucketlists/?q=name/` | `GET` | searches a bucketlist by the name|
| `/bucketlists/<id>/` | `GET` |  Retrieve a bucketlist by ID|
| `/bucketlists/<id>/` | `PUT` | Update a bucketlist |
| `/bucketlists/<id>/` | `DELETE` | Delete a bucketlist |
| `/bucketlists/<id>/items/` | `POST` |  Create items in a bucketlist |
| `/bucketlists/<id>/items/<item_id>/` | `DELETE`| Delete an item in a bucketlist|
| `/bucketlists/<id>/items/<item_id>/` | `PUT`| update a bucketlist item details|

## Testing
You can run the tests ``` nosetests --with-coverage```
