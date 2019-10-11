from pathlib import Path
import hashlib

from django.utils import timezone
from django.conf import settings

def hash_file(file, block_size=65536):
    hash_func = hashlib.md5()
    if file.multiple_chunks():
        for chunk in file.chunks(block_size):
            hash_func.update(chunk)
    else:
        hash_func.update(file.read())
    return hash_func.hexdigest()

def get_upload_path(instance, filename):
    date = timezone.now()
    path = Path(filename)
    ext = ''.join(path.suffixes)
    hash_string = hash_file(instance.file)
    instance.hash = hash_string
    instance.filename = filename
    return f'{settings.FILES_PATH}/{date:%Y}/{date:%m}/{date:%d}/{hash_file(instance.file)}{ext}'
