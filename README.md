flask-rest-api-crud-authentication
======================

## Installation
1. To install pyhton library

```
pip install requirements.txt
```

2. Run the app.py

```
python app.py
```

3. Import "Flask" postman collection and "Flask" postman environment in postman

4. Test the CRUD REST API in Postman

## Important note
1. this project support: MYSQL and sqlite.

`Default using sqlite`

if you want to mySQL modify the `SQLALCHEMY_DATABASE_URI` to using "mysql://root:@localhost/customer" and open xampp  Apache and MySQL

```
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/customer"
```

## postman collection
this is the postman collection and environment. Inside the postman collection including unit test.

1. import Customer.postman environment to postman: [postman_environment.json](https://drive.google.com/file/d/19sTbQymseWh4Eu-P4nrcSbPlJSDaHRQT/view?usp=drive_link)

2. import flask postman collection to test the crud api: [postman_collection.json](https://drive.google.com/file/d/1ZDZb-cndVlOnqqMQr9_huQ_B4MDbGEQD/view?usp=drive_link)


## how to run the postman collection test

1. open postman

2. import "Flask" postman collection in postman

2. import "Flask" postman environment in postman

4. Run Collection

5. Run Flask

