#!/bin/sh

pip_install:
	pip install Flask
	pip install Flask-Script
	pip install Flask-RESTful
	pip install Flask-HTTPAuth
	pip install SQLAlchemy
	pip install passlib

init-db:
	python manage.py init_db

dev-run:
	python manage.py runserver

init: pip_install init-db
run: dev-run
