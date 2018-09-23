from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from upload.forms import *


def home(request):
    if request.method == 'POST':
        form = UploadVideoForm(request.POST)
        if form.is_valid:
            form.save()
        return HttpResponse("Good job!")
    else:
        form = UploadVideoForm()
        args = {'form': form}
        return render(request, 'upload_form.html', args)
