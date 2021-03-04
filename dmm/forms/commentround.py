from django.forms import ModelForm
from django import forms
from ..models import Comment, Expert, Specie, TonalType, Tag, CommentRound


class CommentRoundForm(ModelForm):
    clarification = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        initial='Текст комментария')
    comment = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        queryset=Comment.objects.all(),
        initial={'max_number': '1'}
    )
    expert = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        queryset=Expert.objects.all(),
        initial={'max_number': '1'}
    )
    specie = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        queryset=Specie.objects.all(),
        initial={'max_number': '1'}
    )
    tonal_type = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        queryset=TonalType.objects.all(),
        initial={'max_number': '1'}
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": 'my_class'})
    )

    def set_initial(self, comment):
        self.comment = comment

    class Meta:
        model = CommentRound
        exclude = ()
        fields = ('clarification', 'comment', 'expert', 'specie', 'tonal_type', 'tags')
