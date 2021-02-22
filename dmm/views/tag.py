from .default_imports import *
from ..models import Tag
from ..helpers.tag import *


class AddTagView(View):
    def post(self, request):
        if request.is_ajax():
            tag_name = request.POST.get('tag_name')
            tag_description = request.POST.get('tag_description')
            tag_is_common = request.POST.get('tag_is_common')
            tag_expert_id = request.POST.get('tag_expert_id')
            tag_checked_ids = [int(spec_id) for spec_id in json.loads(request.GET.get('tag_checked_ids'))]

            comment_instance_id = ''
            Tag(name=tag_name, description=tag_description, is_common=(tag_is_common == 'true'), expert_id=tag_expert_id).save()
            logger.info(request.user.expert.name + ' tries to insert tag')
            logger.info(request.user.expert.name +
                        ' successfully inserted tag ' + t.name)

            tags_section = render_to_string(
                'dmm/tag/_tag_section.html',
                {'comment_instance_id': comment_instance_id,
                 'specific_tags': get_specific_tags(),
                 'common_tags': get_common_tags(),
                 'tag_checked_ids': tag_checked_ids
                 })
            return JsonResponse({'tags_section': tags_section}, status=200)
        return render(request, 'dmm/statistics.html')
