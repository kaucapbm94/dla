import logging
from django import template

register = template.Library()
logger = logging.getLogger(__name__)


@register.filter
def return_item(l, i):
    try:
        return l[i]
    except:
        return None
