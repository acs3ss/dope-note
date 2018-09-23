<<<<<<< HEAD
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, PasswordResetForm
from .forms import RegistrationForm, EditProfileForm, EditUserProfileForm
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("account:view-profile")
    else:
        form = RegistrationForm()
        args = {'form': form}
        return render(request, 'signup.html', args)

def view_profile(request):
    user = request.user.userprofile
    my_classes = user.class_set.all()
    my_videos = user.video_set.all()
    args = {'user': user,
            'my_classes': my_classes,
            'my_videos': my_videos,
            }
    return render(request, 'profile.html', args)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        form2 = EditUserProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid() and form2.is_valid():
            form.save()
            data = form2.cleaned_data
            profile = UserProfile.objects.get(user=request.user)
            profile.image = data['image']
            profile.phone_number = data['phone_number']
            profile.address = data['address']
            profile.date_of_birth = data['date_of_birth']
            profile.save()
            return redirect("accounts:view-profile")
    else:
        form = EditProfileForm(instance=request.user)
        form2 = EditUserProfileForm(instance=request.user.userprofile)
        args = {'form': form, 'form2': form2}
        return render(request, 'edit_profile.html', args)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/account/profile')
        else:
            return redirect('account/change_password')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'change_password.html', args)
