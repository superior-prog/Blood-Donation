from django import forms
from .models import *
from django.forms import ModelForm


class PostRequestForm(ModelForm):
    needed_within = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = RequestModel
        fields = '__all__'
        exclude = ['user']
