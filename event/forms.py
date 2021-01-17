from django import forms
from .models import *
from django.forms import ModelForm


class CreateEventForm(ModelForm):
    start_datetime = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_datetime = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    image = forms.ImageField(required=False, error_messages={'invalid': "Image files only"}, widget=forms.FileInput)

    class Meta:
        model = EventModel
        fields = '__all__'
        exclude = ['host']
