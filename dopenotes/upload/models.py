from django.db import models
from django.contrib.auth.models import User

# Video
class Video(models.Model):
    title = models.CharField(max_length=128)
    url = models.CharField(max_length=2048)
    text = models.TextField(max_length=None)
    extra_content = models.TextField(max_length=None)

    def __str__(self):
        return str(self.url)


# Users
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    videos = models.ForeignKey(Video, on_delete=models.DO_NOTHING)

class Class(models.Model):
    name = models.CharField(max_length=128)
    students = models.ForeignKey(User, on_delete=models.DO_NOTHING)