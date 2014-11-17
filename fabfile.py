# encoding: utf-8

from os.path import dirname, join, realpath

from fabric.context_managers import lcd
from fabric.decorators import task
from fabric.operations import local
from fabric.tasks import execute
from app.settings import DATABASES


_current_dir = dirname(realpath(__file__))


def _mysql_command(sql):
    db = DATABASES['default']
    return local(
        'echo "%s" | mysql --batch --user=%s --password=%s' %
        (sql, db['USER'], db['PASSWORD']))


@task
def drop_database():
    """
    Drop and create database.
    """
    local("echo 'DROP DATABASE stwa;' | python ./manage.py dbshell")


@task
def create_database():
    """
    Create database with devdata, create superuser.
    """

    # create database
    _mysql_command(
        'CREATE DATABASE %s CHARACTER SET utf8 COLLATE utf8_general_ci;' %
        DATABASES['default']['NAME'])

    local("./manage.py migrate -v0 --no-initial-data")
    local("./manage.py syncdb --noinput -v0")
    local("./manage.py createcachetable cache_default")
    execute(create_superuser)
    local("./manage.py loaddata devdata initial_data -v0")


@task
def create_database_role():
    """
    Creates database role for django app.
    """
    db = DATABASES['default']

    sql = "CREATE USER '%s'@'localhost' IDENTIFIED BY '%s';" % \
          (db['USER'], db['PASSWORD'])
    sql += "GRANT ALL PRIVILEGES ON *.* TO '%s'@'localhost'" \
           " WITH GRANT OPTION;" % db['USER']
    local('echo "%s" | mysql -u root -p' % sql)


@task
def create_superuser(username='admin', password='a'):
    """
    Create superuser with given username (or "admin") and password (or "a").
    """
    local("./manage.py createsuperuser --noinput --username %s "
          "--email %s@example.pl" % (username, username))
    local("./manage.py set_password %s %s" % (username, password))


@task
def install_requirements():
    """
    Install pip and bower requirements.
    """
    local("pip install -r requirements.txt")
    local("bower install")


@task
def recreate_database():
    """
    Drop and create database, run syncdb and migrations, create superuser.
    """
    execute(drop_database)
    execute(create_database)


@task(alias='migrate')
def syncdb():
    """
    Migrate database and load initial and dev data
    """
    local("./manage.py migrate -v0")
    local("./manage.py loaddata devdata initial_data -v0")
