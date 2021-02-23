from django.forms import ModelForm
from dmm.models import Tag


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = [
            "name",
            "description",
            "is_common",
            "expert"
        ]
