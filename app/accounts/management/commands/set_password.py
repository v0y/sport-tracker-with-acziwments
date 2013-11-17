# encoding: utf-8

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, username, password='a', **options):
        u = User.objects.get(username=username)
        u.set_password(password)
        u.save()
