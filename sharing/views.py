from django.db.models import QuerySet
from django.http import FileResponse
from django.shortcuts import render

from sharing.forms import FileForm, PasswordForm
from sharing.models import SharedFile

# TODO: Make drag and drop fileupload: https://www.smashingmagazine.com/2018/01/drag-drop-file-uploader-vanilla-js/


def index(request):
    form = FileForm(request.POST or None, request.FILES or None)
    # svg = make_qrcode_svg("link", size=40)
    if request.POST:
        if form.is_valid():
            file = form.save()
            return render(request, 'sharing/share_link.html', {'file': file})
    context = {
        'form': form,
        #   'svg': svg
    }
    return render(request, 'sharing/sharedfile_form.html', context)


def get_by_hash(request, url_hash):
    """Check if file exists and check password"""
    qs: QuerySet = SharedFile.objects.filter(url_hash__iexact=url_hash)
    if not qs.exists():
        return render(request, 'sharing/file_not_found.html')
    file: SharedFile = qs.first()
    if file.password:
        form = PasswordForm(request.POST or None)
        if request.POST and form.is_valid():
            if file.check_password(form.cleaned_data['password']):
                return serve_file(request, file)
            form.add_error('password', 'Incorrect password')
        return render(request, 'sharing/password_form.html', {'form': form})
    return serve_file(request, file)


def serve_file(request, file):
    """return file as attachment"""
    response = FileResponse(file.file, as_attachment=True, filename=file.filename)
    if file.burn_after_open:
        file.delete()
    return response
