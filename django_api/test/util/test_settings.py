"""
Django config for django-config project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of config and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
# include all normal settings
from django_api.src.config.settings import *

# override test specific settings
NEO4J_BOLT_URL = "bolt://neo4j:testpassword@localhost:7688"