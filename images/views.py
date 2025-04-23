

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

def folder_list(request):
    # Get list of folders in the media/pictures directory
    base_dir = os.path.join(settings.MEDIA_ROOT, 'pictures')
    folders = [folder for folder in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, folder))]
    return render(request, 'images/folder_list.html', {'folders': folders})

def image_list_folder(request, folder_name):
    # Get list of pictures in the selected folder
    folder_path = os.path.join(settings.MEDIA_ROOT, 'pictures', folder_name)
    if not os.path.exists(folder_path):
        return render(request, '404.html')  # Handle folder not found
    images = []
    for img in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, img)):
            images.append({
                'name': img.removesuffix(".png").removesuffix(".jpg")[0:21],
                'path': f"{settings.MEDIA_URL}pictures/{folder_name}/{img}",
                'info': folder_name + '+' + img
            })
    return render(request, 'images/image_list_folders.html', {'folder_name': folder_name, 'test': images})



def download_image_folder(request, filename):
    file_info = filename.split('+')
    file_path = os.path.join(settings.MEDIA_ROOT, 'pictures', file_info[0], file_info[1])
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True)
    else:
        raise Http404("Image not found")