
from django.db import models
from django.utils import timezone

from filesharing.settings import FILES_PATH

from .utils import hash_file, get_upload_path


class SharedFile(models.Model):
    uploaded = models.DateTimeField()
    file = models.FileField(upload_to=get_upload_path)
    filename = models.CharField(max_length=100, null=True, blank=True)
    hash = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.filename
