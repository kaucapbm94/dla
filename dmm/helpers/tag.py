from ..models import Tag


def get_specific_tags():
    return Tag.objects.filter(is_common=False)


def get_common_tags():
    return Tag.objects.filter(is_common=True)
