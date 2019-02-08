from django import template

register = template.Library()


def dictLenght(value):
    if(type(value) is dict):
        nb = 0
        for keys in value:
            for val in value[keys]:
                nb += 1
    return nb


register.filter('dictLenght', dictLenght)
