# encoding: utf-8

from hashlib import sha1
import time

from django.db import models


class SHA1TokenMixin(models.Model):
    token = models.CharField(verbose_name=u'token', max_length=40, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # create hash based on time
        if not self.token:
            self.token = sha1(str(time.time())).hexdigest()

        # run normal save
        return super(SHA1TokenMixin, self).save(*args, **kwargs)


class CreatedAtMixin(models.Model):
    created_at = models.DateTimeField(
        verbose_name=u'czas utworzenia', auto_now_add=True
    )

    class Meta:
        abstract = True
