# encoding: utf-8

from os.path import dirname, join, realpath

from fabric.context_managers import lcd
from fabric.operations import local
from fabric.tasks import execute


_current_dir = dirname(realpath(__file__))


def drop_database():
    """
    Drop and create database.
    """
    local("echo 'DROP DATABASE stwa;' | python ./manage.py dbshell")


def create_database():
    """
    Create database with devdata, create superuser.
    """
    # create database
    sql = 'CREATE DATABASE stwa ' \
          'CHARACTER SET utf8 COLLATE utf8_general_ci;'
    local("echo '%s' | python ./manage.py dbshell" % sql)

    # sync
    local("./manage.py syncdb --noinput -v0")
    local("./manage.py migrate -v0 --no-initial-data")

    execute(create_superuser)

    # load data
    local("./manage.py loaddata devdata initial_data -v0")


def create_superuser(username='admin', password='a'):
    """
    Create superuser with given username (or "admin") and password (or "a").
    """
    local("./manage.py createsuperuser --noinput --username %s "
          "--email %s@example.pl" % (username, username))
    local("./manage.py set_password %s %s" % (username, password))


def install_requirements():
    """
    Install pip and bower requirements.
    """
    local("pip install -r requirements.txt")
    local("./manage.py bower_install")


def lets_rock():
    """
    Install all required packages and create database.
    """
    # Node.js
    local("curl http://nodejs.org/dist/node-latest.tar.gz | tar xvz")
    with lcd(join(_current_dir, "node-v*")):
        local("./configure --prefix=$VIRTUAL_ENV")
        local("make install")

    # npm
    local("curl https://npmjs.org/install.sh | sh")

    # npm requirements
    local("cat npm-requirements.txt | xargs -I % npm install %")

    # Install pip and bower requirements
    execute(install_requirements)

    execute(create_database)


def recreate_database():
    """
    Drop and create database, run syncdb and migrations, create superuser.
    """
    execute(drop_database)
    execute(create_database)
