from django import template
from django.template.defaultfilters import stringfilter
from wappuheila import settings

register = template.Library()
AVAILABLE_LOGOS = {'facebook' : 'f_logo.png',
                   'google-oauth2' : 'g_logo.png'}
@register.filter
@stringfilter
def to_social_logo_url(value):
    try:
        return settings.STATIC_URL + AVAILABLE_LOGOS[value]
    except KeyError:
        return settings.STATIC_URL + "not_found.png"