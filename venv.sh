#!/bin/bash
virtualenv venv
source venv/bin/activate
pip install --upgrade pip
pip install Pillow
pip install Django==1.10
pip install django-friendship
pip install djangorestframework
pip install requests