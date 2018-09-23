from django.shortcuts import get_object_or_404, render
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.urls import reverse

from upload.forms import *


def home(request):
    if request.method == 'POST':
        form = UploadVideoForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('upload:detail', args=(form.cleaned_data['url'],)))
    else:
        form = UploadVideoForm()
        args = {'form': form}
        return render(request, 'upload_form.html', args)

def video_detail_view(request, url=None):
    obj = get_object_or_404(Video, url=url)
    args = {'url': obj}
    return render(request, 'detail_view.html', args)
