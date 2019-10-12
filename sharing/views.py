from django.shortcuts import render

from sharing.forms import FileForm
from sharing.utils import make_qrcode_svg

def index(request):
    form = FileForm(request.POST or None, request.FILES or None)
    # svg = make_qrcode_svg("link", size=40)
    if request.POST:
        if form.is_valid():
            form.save()
    context = {
        'form': form,
    #   'svg': svg
    }
    return render(request, 'sharing/sharedfile_form.html', context)
