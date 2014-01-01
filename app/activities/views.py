# encoding: utf-8

from django.template.loader import render_to_string


def render_activities(activities_list):
    """
    Render activities messages

    :return: list of rendered htmls
    """
    rendered_activities_list = []

    for activity in activities_list:
        template = 'activities/%s/body.html' % activity.type.label
        activity.data_json.update({'user': activity.user})

        rendered_activity = render_to_string(template, activity.data_json)
        rendered_activities_list.append(rendered_activity)

    return rendered_activities_list
