from django.template.defaulttags import register
import logging
import json
import math
logger = logging.getLogger(__name__)


@register.filter
def needs_new_column(params, iter):
    params = json.loads(params)
    iter = int(iter)
    threshold = math.ceil(params['collection_size'] / params['column_number'])
    return True if iter % threshold == 0 and iter != 0 else False
