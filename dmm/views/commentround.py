from ..models import Expert, CommentRound, CommentRoundTags, CommentTags
from django.shortcuts import render, redirect


def CommentRoundShow(request, comment_round_id):
    expert_id = request.user.expert.id
    expert = Expert.objects.get(id=expert_id)
    comment_round = CommentRound.objects.get(id=comment_round_id)
    comment_round_tags = CommentRoundTags.objects.filter(comment_round=comment_round)
    comment_tags = CommentTags.objects.filter(comment=comment_round.comment)
    context = {
        'comment_tags': comment_tags,
        'comment_round': comment_round,
        'comment_round_tags': comment_round_tags,
        'expert': expert
    }
    return render(request, "dmm/comment_round/show.html", context)
