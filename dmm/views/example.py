from django.shortcuts import render
from django.forms import modelformset_factory
from ..models import Example
import logging
logger = logging.getLogger(__name__)


def index(request):
    ExampleFormSet = modelformset_factory(Example, fields=('name', 'location'), extra=2)

    if request.method == 'POST':
        form = ExampleFormSet(request.POST)
        # instances = form.save(commit=False)

        # for instance in instances:
        #     instance.save()

        instances = form.save()

    # form = ExampleFormSet(queryset=Example.objects.none())
    form = ExampleFormSet()
    logger.debug(form)
    return render(request, 'dmm/index.html', {'form': form})
