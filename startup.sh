#!/bin/bash
python manage.py collectstatic && gunicorn --workers 2 ecommerce.wsgi