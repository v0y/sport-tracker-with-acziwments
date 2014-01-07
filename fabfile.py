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

    local("./manage.py syncdb --noinput -v0")
    local("./manage.py migrate -v0 --no-initial-data")
    execute(create_superuser)
    local("./manage.py loaddata devdata initial_data -v0")


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
def install_host_requirements():
    """
    Install pip and npm host requirements.
    """
    local("pip install -r host-requirements.txt")
    local("cat npm-host-requirements.txt | xargs -I % sudo npm install % -g")


@task
def install_npm_requirements():
    """
    Install npm requirements.
    """
    local("cat npm-requirements.txt | xargs -I % sudo npm install %")


@task
def install_requirements():
    """
    Install pip and bower requirements.
    """
    local("pip install -r requirements.txt")
    execute(install_npm_requirements)
    local("./manage.py bower_install")


@task
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

    # Install pip and bower requirements
    execute(install_requirements)

    # database
    execute(create_database_role)
    execute(create_database)


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
    Migrate database (syncdb + migrate)
    """
    local("./manage.py syncdb --noinput -v0")
    local("./manage.py migrate -v0 --no-initial-data")
    local("./manage.py loaddata devdata initial_data -v0")
