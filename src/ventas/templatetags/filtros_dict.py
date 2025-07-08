from django import template

register = template.Library()

@register.filter
def dictkey(diccionario, clave):
    return diccionario.get(clave, 0)