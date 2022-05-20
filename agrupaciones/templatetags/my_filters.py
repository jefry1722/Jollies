from django import template

register = template.Library()

@register.filter(name='times')
def times(number):
    if number == '':
        number=0
    return range(int(number))

@register.filter(name='currency')
def currency(number):
    return "{:,}".format(int(number)).replace(",", ".")\

@register.filter(name='phonenumber')
def phonenumber(telefono):
    first = str(telefono)[0:3]
    second = str(telefono)[3:6]
    third = str(telefono)[6:10]
    phone = first + '-' + second + '-' + third
    return phone