import hashlib
from uuid import uuid4

from django.utils import timezone
from django.conf import settings
import qrcode
from qrcode.image.svg import SvgPathImage


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
    hash_string = hash_file(instance.file)
    instance.file_hash = hash_string
    instance.filename = filename
    return f'{settings.FILES_PATH}/{date:%Y}/{date:%m}/{date:%d}/{hash_string}'

def make_url_hash():
    return uuid4().hex

def make_qrcode_svg(text: str, size=40):
    qr = qrcode.QRCode(box_size=size, border=4, image_factory=SvgPathImage)
    qr.add_data(text)
    qr.make(fit=True)
    qr_code = qr.make_image()
    file_redirect = FileRedirect()
    qr_code.save(file_redirect)
    return file_redirect.text


class FileRedirect:
    """Class for redirecting fileIO to string when generating QR code"""
    text = ''

    def write(self, text):
        print(text)
        self.text += text.decode()

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.__str__()
