# encoding: utf-8

from annoying.fields import JSONField
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from app.shared.models import (
    CreatedAtMixin,
    RelatedDateMixin,
)
from app.workouts.models import Workout


class ActivityType(models.Model):
    label = models.SlugField(max_length=64)
    description = models.CharField(max_length=128, blank=True, null=True)

    def __unicode__(self):
        return self.label


class Activity(CreatedAtMixin, RelatedDateMixin):
    type = models.ForeignKey('ActivityType')
    user = models.ForeignKey(User)
    data_json = JSONField(default={})

    def __unicode__(self):
        return '%s dla %s' % (self.type.label, self.user)


@receiver(post_save, sender=Workout)
def create_new_workout_notice(sender, instance, created, **kwargs):
    if created:
        Activity.objects.create(
            type=ActivityType.objects.get(label='new_workout'),
            user=instance.user,
            related_date=instance.datetime_start,
            data_json={
                'workout_name': unicode(instance),
                'workout_url': instance.get_absolute_url(),
                'workout_duration': instance.duration_visible
            }
        )
