# Requirements
```
pip install pipenv
```
then 
```
pipenv install
```

# MySQL setup
## Log into MySQL as root
```
mysql -u root
```
## Create database
```
CREATE DATABASE dbms_project;
```

# Serve
```
pipenv run uvicorn main:app [--reload]
```
