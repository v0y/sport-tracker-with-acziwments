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
    Create database with devdata, create superuser.
    """
    local("./manage.py syncdb --noinput -v0")
    local("./manage.py migrate -v0")
    execute(create_superuser)
    local("./manage.py loaddata devdata -v0")


def create_superuser(username='admin', password='a'):
    """
    Create superuser with given username (or "admin") and password (or "a").
    """
    local("./manage.py createsuperuser --noinput --username %s "
          "--email %s@example.pl" % (username, username))
    local("./manage.py set_password %s %s" % (username, password))


def recreate_database():
    """
    Drop and create database, run syncdb and migrations, create superuser.
    """
    execute(clear_database)
    execute(create_database)
