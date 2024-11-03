from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone


class Participant(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, primary_key=True)
    updated_at = models.DateTimeField(auto_now = True, blank = True)
    interaction_mode = models.CharField(max_length=20, default='tutor_asks')  # 'tutor_asks' or 'student_asks'
    def __unicode__(self):
        return 'id='+ str(self.pk)

class Assistant(models.Model):
    assistant_id = models.TextField(verbose_name = "Assistant ID")
    video_name = models.CharField(verbose_name= "videoname", default = '', max_length=100)
    vector_store_id = models.TextField(verbose_name='Vector store ID')
    file_id = models.TextField(verbose_name='File ID', null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, primary_key=True)


class Message(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    sender = models.CharField(max_length=10)  # 'user' or 'assistant'
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)