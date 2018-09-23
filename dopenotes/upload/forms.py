from django import forms
from django.db import transaction
from upload.models import *
from django.forms import ModelForm

class UploadVideoForm(ModelForm):

    class Meta:
        model = Video
        fields = ['url', 'clazz']

class CreateClassForm(ModelForm):

    class Meta:
        model = Class
        fields = ['name']

class JoinClassForm(forms.Form):
    classes = forms.MultipleChoiceField(choices=())
