from .default_imports import *
from ..models import *


@login_required(login_url='login')
@allowed_users(allowed_roles=['expert', 'admin'])
def MarkupCommentPage(request, result_id):
    expert_id = request.user.expert.id
    expert = Expert.objects.get(user=request.user)
    species = Specie.objects.all()
    tags = Tag.objects.all()
    content_types = ContentType.objects.all()
    resource_types = ResourceType.objects.all()
    language_types = LanguageType.objects.all()
    tonal_types = TonalType.objects.all()
    date_picker_form = DateTimeModelForm()

    result = Result.objects.get(pk=result_id)
    logger.debug(result)
    comments = get_need_round_comments(result, expert_id)
    logger.debug(comments)

    # tags = Tag.objects.all()
    context = {
        'result': result,
        'comments': comments,
        'expert': expert,
        'species': species,
        'tonal_types': tonal_types,
        'tags': tags,
        'content_types': content_types,
        'resource_types': resource_types,
        'language_types': language_types,
        'date_picker_form': date_picker_form,
        'comment_instance_id': '',
        'specific_tags': Tag.objects.filter(is_common=False),
        'common_tags': Tag.objects.filter(is_common=True),
        'tag_checked_ids': []
    }

    return render(request, 'dmm/comment/sample_and_markup/main.html', context)


@ login_required(login_url='login')
@ allowed_users(allowed_roles=['expert', 'admin'])
def SampleMarkupCommentPage(request):
    expert = Expert.objects.get(user=request.user)
    species = Specie.objects.all()
    tags = Tag.objects.all()
    content_types = ContentType.objects.all()
    resource_types = ResourceType.objects.all()
    language_types = LanguageType.objects.all()
    date_picker_form = DateTimeModelForm()

    context = {
        'expert': expert,
        'species': species,
        'tags': tags,
        'content_types': content_types,
        'resource_types': resource_types,
        'language_types': language_types,
        'date_picker_form': date_picker_form,
    }
    return render(request, 'dmm/comment/sample_and_markup/main.html', context)
