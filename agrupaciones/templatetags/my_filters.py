from django import template

register = template.Library()

@register.filter(name='times')
def times(number):
    if number == '':
        number=0
    return range(int(number))

@register.filter(name='currency')
def currency(number):
    return "{:,}".format(int(number)).replace(",", ".")