from django.shortcuts import get_object_or_404, render
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.forms.utils import ErrorList
from django.views.generic import TemplateView
from django.urls import reverse

from upload.forms import *

def index(request):
    if request.method == 'POST':
        form = UploadVideoForm(request.POST, error_class=DivErrorList)
        if form.is_valid():
            video = Video(url=form.cleaned_data['url'], user=request.user.userprofile)
            video.save()
            return HttpResponseRedirect(reverse('upload:detail', args=(video.pk,)))
        return render(request, 'upload_form.html', {'form': form})
    else:
        form = UploadVideoForm(error_class=DivErrorList)
        args = {'form': form}
        return render(request, 'upload_form.html', args)


def video_detail_view(request, pk=None):
    obj = get_object_or_404(Video, pk=pk)
    args = {'url': obj}
    return render(request, 'detail_view.html', args)


# Create Class
def create_class(request):
    if request.method == 'POST':
        form = CreateClassForm(request.POST)
        if form.is_valid():
            clazz = form.save()
            clazz.students.add(request.user.userprofile)
            return HttpResponseRedirect(reverse('account:view-profile'))
        return render(request, 'create_class_form.html', {'form': form})
    else:
        form = CreateClassForm()
        args = {'form': form}
        return render(request, 'create_class_form.html', args)

def join_class(request):
    if request.method == 'POST':
        form = JoinClassForm(request.POST)
        if form.is_valid():
            clazz = form.save()
            clazz.students.add(request.user.userprofile)
            return HttpResponseRedirect(reverse('account:view-profile'))
        return render(request, 'join_class_form.html', {'form': form})
    else:
        form = JoinClassForm({'classes': tuple(request.user.userprofile.class_set.all())})
        args = {'form': form}
        return render(request, 'join_class_form.html', args)

class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()
    def as_divs(self):
        if not self:
            return ''
        return '<ul class="alert alert-danger" role="alert">%s</ul>' % '\n'.join(['<li>%s</li>' % e for e in self])
