from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    file = models.FileField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="note_owner")

    def __str__(self):
        return self.created.date()
