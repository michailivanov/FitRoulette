from django import forms
from .models import Exercise, CardSet


class AddExerciseForm(forms.ModelForm):
    name = forms.CharField(label="Название упражнения", required=True)
    image = forms.ImageField(label="Изображение", required=True)
    class Meta:
        model = Exercise
        fields = ['name', 'image']



class AddCardSetForm(forms.ModelForm):
    name = forms.CharField(label="Название набора", required=True)
    exercises = forms.ModelMultipleChoiceField(
        label = 'Упражнения',
        widget = forms.CheckboxSelectMultiple,
        queryset = Exercise.objects.all(),
        required = True,
    )
    class Meta:
        model = CardSet
        fields = ['name', 'exercises']
