from django.db import models
from django.contrib.auth.models import User

class Video(models.Model):
    title = models.CharField(max_length=128)
    url = models.URLField('URL', max_length=2048, unique=True)
    keywords = models.TextField(max_length=None)
    transcription = models.TextField(max_length=None)
    resources = models.TextField(max_length=None)
    user = models.ForeignKey('account.UserProfile', on_delete=models.CASCADE, null=True)
    clazz = models.ForeignKey('Class', on_delete=models.CASCADE, null=True, verbose_name='Class', help_text='Register in classes in your user profile')
    text = models.TextField(max_length=None)
    extra_content = models.TextField(max_length=None)

    def __str__(self):
        return str(self.url)


class Class(models.Model):
    name = models.CharField(max_length=128)
    students = models.ManyToManyField('account.UserProfile')

    def __str__(self):
        return str(self.name)
