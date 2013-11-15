# encoding: utf-8

from fabric.operations import local
from fabric.tasks import execute


def clear_database():
    """
    Drop and create database.
    """
    sql = 'DROP DATABASE stwa; ' \
          'CREATE DATABASE stwa ' \
          'CHARACTER SET utf8 COLLATE utf8_general_ci;'
    local("echo '%s' | python ./manage.py dbshell" % sql)


def create_database():
    """
    Create database, run migrations, create superuser "admin".
    """
    local("./manage.py syncdb --noinput -v0")
    local("./manage.py migrate")
    execute(create_superuser)


def create_superuser(username='admin'):
    """
    Create superuser with given username or "admin".
    """
    local("./manage.py createsuperuser --username %s --email %s@example.pl"
        % (username, username))


def recreate_database():
    """
    Drop and create database, run syncdb and migrations, create
    superuser.
    """
    execute(clear_database)
    execute(create_database)
