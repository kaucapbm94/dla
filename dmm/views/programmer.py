from django.shortcuts import render, redirect
from django.forms import modelformset_factory, inlineformset_factory
from ..models import Programmer, Language
from ..forms import ProgrammerForm
import logging
logger = logging.getLogger(__name__)


def programmer_new(request):

    # LanguageFormset = modelformset_factory(Language, fields=('name',))
    LanguageFormset = inlineformset_factory(Programmer, Language, fields=('name', ), can_delete=False, extra=3, max_num=3)

    if request.method == 'POST':
        logger.debug(request.POST)
        form = ProgrammerForm(request.POST)
        logger.debug(form)
        programmer = form.save()
        logger.debug(programmer)
        # formset = LanguageFormset(request.POST, queryset=Language.objects.filter(programmer_id=programmer.id))
        formset = LanguageFormset(request.POST, instance=programmer)
        if formset.is_valid():
            formset.save()
            # instances = formset.save(commit=False)
            # for instance in instances:
            #     instance.programmer_id = programmer.id
            #     instance.save()
            return redirect('programmer_new')
    form = ProgrammerForm(request.GET)
    # formset = LanguageFormset(queryset=Language.objects.filter(programmer_id=programmer.id))
    formset = LanguageFormset()

    return render(request, 'dmm/programmer.html', {'formset': formset, 'form': form})


def programmer(request, programmer_id):
    programmer = Programmer.objects.get(pk=programmer_id)
    # LanguageFormset = modelformset_factory(Language, fields=('name',))
    LanguageFormset = inlineformset_factory(Programmer, Language, fields=('name', ), can_delete=False, extra=1, max_num=3)

    if request.method == 'POST':
        # formset = LanguageFormset(request.POST, queryset=Language.objects.filter(programmer_id=programmer.id))
        formset = LanguageFormset(request.POST, instance=programmer)
        if formset.is_valid():
            formset.save()
            # instances = formset.save(commit=False)
            # for instance in instances:
            #     instance.programmer_id = programmer.id
            #     instance.save()
            return redirect('programmer', programmer_id=programmer.id)

    # formset = LanguageFormset(queryset=Language.objects.filter(programmer_id=programmer.id))
    formset = LanguageFormset(instance=programmer)

    return render(request, 'dmm/programmer.html', {'formset': formset})
