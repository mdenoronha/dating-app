# https://stackoverflow.com/questions/8000022/django-template-how-to-look-up-a-dictionary-value-with-a-variable
from django.template.defaulttags import register

@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)