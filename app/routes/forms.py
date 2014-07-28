# encoding: utf-8

from django import forms
from django.forms.models import ModelForm

from .models import Route


class RouteIdMixin(ModelForm):
    route_id = forms.IntegerField(required=False, widget=forms.HiddenInput())

    def clear_route_id(self):
        if self.cleaned_data['route_id']:
            route_id = self.cleaned_data['route_id']
            if Route.objects.filter(id=route_id).exists():
                return route_id
            else:
                raise forms.ValidationError("Non-existent route id supplied.")

    def assign_route_to_workout(self, workout):
        # get route
        route_id = self.cleaned_data['route_id']
        if route_id:
            route = Route.objects.get(id=route_id)


            # update route properties if needed
            route.start_time = workout.datetime_start
            route.finish_time = workout.datetime_stop
            route.length = workout.distance

            # save
            route.workout = workout
            route.save()
