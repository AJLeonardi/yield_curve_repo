from django.template import Library
from django.conf import settings

register = Library()

@register.simple_tag(takes_context=True)
def yc_app_version(context):
    return settings.APP_VERSION
