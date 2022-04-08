import os
import urllib
from io import BytesIO
import requests
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from PIL import Image
from .models import Photo
from django.core.files import File
from config.settings import MEDIA_ROOT, UPLOAD_TO


class PhotosViewSet(viewsets.ViewSet):
    """
     ViewSet для работы с изображениями.
    """

    def list(self, request):
        """ Получить все изображения """
        photos = Photo.objects.all()
        new_list = list(map(Photo.to_json, photos))
        return Response(new_list)

    def retrieve(self, request, pk=None):
        """ Получить одно изображение """
        try:
            photo = Photo.objects.get(id=pk)
        except Photo.DoesNotExist:
            return Response('Изображение не найдено')
        return Response(photo.to_json())

    def create(self, request):
        """ Добавить изображение """
        if request.FILES.get('file'):
            img = Image.open(request.FILES.get('file'))
            width, height = img.size
            photo = Photo.objects.create(name=request.FILES.get('file').name,
                                         width=width, height=height, picture=request.FILES.get('file'))
        elif request.POST.get('url'):
            url = request.POST.get('url')
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            width, height = img.size
            photo = Photo.objects.create(name=os.path.basename(url), width=width, height=height, url=url)

            result = urllib.request.urlretrieve(url)
            photo.picture.save(
                os.path.basename(url),
                File(open(result[0], 'rb'))
            )
            photo.save()
        return Response(photo.to_json())

    def destroy(self, request, pk=None):
        """ Удалить изображение """
        try:
            photo = Photo.objects.get(id=pk)
            if photo.picture:
                photo.picture.delete(save=True)
            photo.delete()
            return Response(None)
        except Photo.DoesNotExist:
            return Response('Изображение не найдено')

    @action(methods=['post'], detail=True)
    def resize(self, request, pk=None):
        try:
            photo = Photo.objects.get(id=pk)
        except Photo.DoesNotExist:
            return Response('Изображение не найдено')
        width = request.POST.get('width', photo.width)
        height = request.POST.get('height', photo.height)
        if request.POST.get('width') or request.POST.get('height'):
            photo.width = width
            photo.height = height
            photo.save()
            img = Image.open(photo.picture)
            new_image = img.resize((int(width), int(height)))
            save_to = MEDIA_ROOT + '/' + UPLOAD_TO + '/' + os.path.basename(str(photo.picture))
            new_image.save(save_to)
            return Response(photo.to_json())
        else:
            return Response('Нет данных')

