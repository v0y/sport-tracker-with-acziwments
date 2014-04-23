# coding: utf-8

#: selection for sex field
SEX_SELECT = (
    ('K', u'Kobieta'),
    ('M', u'Mężczyzna'),
)


class UnitsTypes(object):
    metric = 1
    imperial = 2


#: selection for units field
UNITS_SELECT = (
    (UnitsTypes.metric, u'Metryczne'),
    (UnitsTypes.imperial, u'Imperialne')
)
