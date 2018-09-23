from django.urls import path, re_path
from django.conf.urls import url
from . import views
#from django.contrib.auth.views import login, logout, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

app_name = 'account'
urlpatterns = [
    # Accounts
    path('signup/', views.signup, name='account-signup'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('profile/', views.view_profile, name='view-profile'),
    path('profile/edit/', views.edit_profile, name='edit-profile'),
    # path('change_password/', views.account.change_password, name='change-password'),

    # # Password Reset
    # path('reset_password/', password_reset, {
    #     'template_name': 'accounts/reset_password.html',
    #     'post_reset_redirect': 'accounts:password_reset_done', 
    #     'email_template_name': 'accounts/reset_password_email.html'
    #     }, 
    #     name='reset-password'),

    # path('reset_password/done/', password_reset_done, {
    #     'template_name': 'accounts/reset_password_sent.html'
    #     },
    #     name='password_reset_done'),

    # re_path(r'^reset_password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, {
    #     'post_reset_redirect': 'accounts:password_reset_complete',
    #     'template_name': 'accounts/reset_password_new.html'
    #     }, 
    #     name='password_reset_confirm'),

    # path('reset_password/complete/', password_reset_complete, {
    #     'template_name': 'accounts/reset_password_complete.html'
    #     }, 
    #     name='password_reset_complete'),

    # # Add Details

]