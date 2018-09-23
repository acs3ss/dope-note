from django.db import models
from upload.models import *

# Managers
class UserProfileManager(models.Manager):

     def get_queryset(self):
        return super(UserProfileManager, self).get_queryset()


# Users
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    videos = models.ForeignKey(Video, on_delete=models.DO_NOTHING)
    is_admin = models.BooleanField(default=False)
    image = models.ImageField(upload_to='profile_image', blank=True, null=True)

    # override objects with manager
    objects = UserProfileManager()
