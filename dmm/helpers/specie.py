def specie_is_present(comment, specie):
    return True if CommentRound.objects.filter(comment=comment, specie=specie).count() >= 1 else False
