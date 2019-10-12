from datetime import timedelta

import bcrypt
from django.db import models

from .utils import get_upload_path


class SharedFile(models.Model):
    uploaded = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=get_upload_path)
    filename = models.CharField(max_length=128, blank=True)
    hash = models.CharField(max_length=128, blank=True)
    password = models.CharField(max_length=128, null=True, blank=True, unique=True)
    message = models.TextField(null=True, blank=True, unique=True)
    burn_after_open = models.BooleanField(
        default=False, help_text='Expire link after it is visited once'
    )
    short_identifier = models.SlugField(
        max_length=50,
        blank=True,
        null=True,
        unique=True,
        help_text='[a-zA-Z0-9_-] only',
    )

    VERY_SHORT = timedelta(minutes=10)
    SHORT = timedelta(hours=1)
    MEDIUM = timedelta(days=1)
    LONG = timedelta(days=5)
    DURATION_CHOICES = (
        (None, 'Never'),
        (VERY_SHORT, '10 minutes'),
        (SHORT, '1 hour'),
        (MEDIUM, '24 hours'),
        (LONG, '5 days'),
    )
    burn_after = models.DurationField(null=True, blank=True, choices=DURATION_CHOICES)

    def set_password(self, clear_password: str, commit=True):
        hashed = bcrypt.hashpw(clear_password.encode('utf-8'), bcrypt.gensalt(12))
        self.password = hashed
        if commit:
            self.save()

    def check_password(self, clear_password: str) -> bool:
        return bcrypt.checkpw(clear_password.encode('utf-8'), self.password)

    def __str__(self):
        return self.filename
