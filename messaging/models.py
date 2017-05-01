from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.PROTECT, related_name='received_messages')

    content = models.TextField()

    timestamp = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.content
