from ..helpers import *

from .auth import *
from .statistics import *
from .result import *
from .specie import *
from .tag import *
from .commentround import CommentRoundShow


def handler500(request, *args, **argv):
    response = render_to_response('dmm/statistics.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response
