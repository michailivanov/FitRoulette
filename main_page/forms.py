from django import forms
from .models import Exercise, CardSet


class AddExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите название'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-file-input'}),
        }
        labels = {
            'image': '',
        }


class AddCardSetForm(forms.ModelForm):
    name = forms.CharField(label="Название набора", required=True)
    exercises = forms.ModelMultipleChoiceField(
        label='',
        widget=forms.CheckboxSelectMultiple,
        queryset=Exercise.objects.all(),
    )

    class Meta:
        model = CardSet
        fields = ['name', 'exercises']
