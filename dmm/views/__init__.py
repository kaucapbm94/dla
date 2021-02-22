from .default_imports import *
from ..helpers import *

from .auth import *
from .markup import *
from .statistics import *

from .comment import *
from .comment_round import *
from .language_type import *
from .result import *
from .specie import *
from .tag import *
from .tonal_type import *

from .contact import *
from .example import *
from .programmer import *
from .book import *


def handler500(request, *args, **argv):
    response = render_to_response('dmm/statistics.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response
