from django.db import models
from django.contrib.auth.models import User

# from account.models import *

# Video
class Video(models.Model):
    title = models.CharField(null=True, max_length=128)
    url = models.URLField('URL', max_length=2048, unique=True)
    keywords = models.TextField(null=True, max_length=None)
    transcription = models.TextField(null=True, max_length=None)
    resources = models.TextField(null=True, max_length=None)
    user = models.ForeignKey('account.UserProfile', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.url)


class Class(models.Model):
    name = models.CharField(max_length=128)
    students = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='students')

    def __str__(self):
        return str(self.name)
