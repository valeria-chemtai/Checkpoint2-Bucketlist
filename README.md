# Bucketlist API
According to Merriam-Webster Dictionary,  a Bucket List is a list of things that one has not done before but wants to do before dying.

Bucketlist API is an online flask-resftul API built to help users keep track of their things to do

## Installation and Setup
Clone the repo
```
https://github.com/valeria-chemtai/Checkpoint2-Bucketlist.git
```
Navigate to the root folder
```
cd checkpoint2-Bucketlist
```
create a virtualenv
```
mkvirtualenv bucketlist
```
Inside virtualenv open a postactivate file to store a script for exporting `App_setting`, `secret key` and `database url` by running the command
```
subl $VIRTUAL_ENV/bin/postactivate
```
In the postactivate file add the following and replace the parenthesis in database_url with appropriate owner
```
export SECRET='akjshdkqiu3ye723y42i34'
export DATABASE_URL="postgres://{}@localhost:5432/bucketlist"
export APP_SETTINGS="development"
```
Install the requirements
```
pip install -r requirements.txt
```
Create a postgres database called bucketlist using postman, why? its easy

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
| `/auth/register` | `POST`  | Register a new user|
|  `/auth/login` | `POST` | Login and retrieve token|
| `/v1/bucketlists` | `POST` | Create a new Bucketlist |
| `/v1/bucketlists` | `GET` | Retrieve all bucketlists for user |
| `/v1/bucketlists/?page=1&limit=3` | `GET` | Retrieve three bucketlists per page |
 `/v1/bucketlists/?q=name` | `GET` | searches a bucketlist by the name|
| `/v1/bucketlists/<id>` | `GET` |  Retrieve a bucketlist by ID|
| `/v1/bucketlists/<id>` | `PUT` | Update a bucketlist |
| `/v1/bucketlists/<id>` | `DELETE` | Delete a bucketlist |
| `/v1/bucketlists/<id>/items` | `POST` |  Create items in a bucketlist |
| `/v1/bucketlists/<id>/items/<item_id>` | `DELETE`| Delete an item in a bucketlist|
| `/v1/bucketlists/<id>/items/<item_id>` | `PUT`| update a bucketlist item details|

## Testing
You can run the tests ``` nosetests --with-coverage```
