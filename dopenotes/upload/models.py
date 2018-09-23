from django.db import models
from django.contrib.auth.models import User

# from account.models import *

# Video
class Video(models.Model):
    title = models.CharField(max_length=128)
    url = models.URLField('URL', max_length=2048, unique=True)
    user = models.ForeignKey('account.UserProfile', on_delete=models.CASCADE, null=True)
    text = models.TextField(max_length=None)
    extra_content = models.TextField(max_length=None)

    def __str__(self):
        return str(self.url)


class Class(models.Model):
    name = models.CharField(max_length=128)
    students = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
