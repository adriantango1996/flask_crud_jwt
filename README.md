flask-rest-api-crud-authentication
======================

## Installation
1. To install, either run

```
pip install requirements.txt
```

2. run the app.py

```
python app.py
```


## postman collection
the collecttion inclduing crud rest api and postman unit test

## Important note
this project support: MYSQL and sqlite.

Default using sqlite. 

if you want to mySQL modify the code using "mysql://root:@localhost/customer"
`app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/customer"

`app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Database.db"``


## how to run the postman collection test

1. clone this project

2. import "Flask" collection in postman

3. Run Collection

4. RUn Flask

