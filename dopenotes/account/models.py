from django.db import models
from upload.models import *
from django.db.models.signals import post_save

# Managers
class UserProfileManager(models.Manager):

     def get_queryset(self):
        return super(UserProfileManager, self).get_queryset()


# Users
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    videos = models.ForeignKey(Video, on_delete=models.DO_NOTHING, null=True)
    is_admin = models.BooleanField(default=False)
    image = models.ImageField(upload_to='profile_image', blank=True, null=True)

    # override objects with manager
    objects = UserProfileManager()

# Signal to create UserProfile when a new User is created
def create_profile(sender, **kwargs):
    if kwargs['created']:
        user = kwargs['instance']
        user_profile = UserProfile.objects.create(user=user)
        if user.is_staff:
            user_profile.is_admin = True
            user_profile.save()

post_save.connect(create_profile, sender=User)