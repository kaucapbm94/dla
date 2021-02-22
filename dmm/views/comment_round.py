from .default_imports import *

from ..models import CommentRound, Tag, CommentRoundTags

class InsertCommentRoundView(View):
    def post(self, request):
        if request.is_ajax():
            comment_id = request.POST.get('comment_id')
            specie_id = request.POST.get('specie_id')
            expert_tag_ids = json.loads(request.POST.get('tag_ids'))
            tonal_type_id = request.POST.get('tonal_type_id')

            clarification = request.POST.get('clarification')
            expert_id = request.POST.get('expert_id')
            create_date = timezone.now()
            logger.info(request.user.expert.name + ' tries to insert comment round ')
            comment_round = CommentRound.objects.create(
                comment_id=comment_id,
                specie_id=specie_id,
                tonal_type_id=tonal_type_id,
                clarification=clarification,
                create_date=create_date,
                expert_id=expert_id,
            )

            tag_ids = Tag.objects.all().values_list('id', flat=True)
            for tag_id in tag_ids:
                CommentRoundTags.objects.create(tag=Tag.objects.get(id=tag_id), comment_round=comment_round,
                                                is_present=(True if tag_id in expert_tag_ids else False))

            logger.info(request.user.expert.name + ' successfully inserted comment round for ' + comment_round.comment.text)
            return JsonResponse({'comment_round_id': comment_round.id}, status=200)
        return render(request, 'dmm/statistics.html')