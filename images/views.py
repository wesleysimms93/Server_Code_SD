

# images/views.py
import os
from django.conf import settings
from django.shortcuts import render
from django.http import FileResponse, Http404




def image_list(request):
    image_folder = os.path.join(settings.MEDIA_ROOT, 'pictures')
    images = []

    if os.path.isdir(image_folder):
        for filename in os.listdir(image_folder):
            if filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                images.append(filename)  # Add only the filename, not the full path

    return render(request, 'images/image_list.html', {'images': images})


def download_image(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, 'pictures', filename)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True)
    else:
        raise Http404("Image not found")

