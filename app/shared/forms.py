# encoding: utf-8

from django.forms import extras


class SelectDateWidgetWithNone(extras.SelectDateWidget):

    def create_select(self, name, field, value, val, choices):
        if self.required and val:  # reversed original statement
            choices.insert(0, self.none_value)
        return super(SelectDateWidgetWithNone, self) \
            .create_select(name, field, value, val, choices)
