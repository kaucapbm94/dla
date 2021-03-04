from django.forms import ModelForm
from dmm.models import Specie


class SpecieForm(ModelForm):

    class Meta:
        model = Specie
        fields = [
            "name",
            "description",
            'expert'
        ]
