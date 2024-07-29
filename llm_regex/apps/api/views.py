import os

from django.conf import settings
from rest_framework import viewsets
from .models import UploadedFile
from .serializers import UploadedFileSerializer


class UploadedFileViewSet(viewsets.ModelViewSet):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer

    def perform_create(self, serializer):
        serializer.save()

    def perform_destroy(self, serializer):
        file_path = os.path.join(settings.MEDIA_ROOT, serializer.file.name)
        if os.path.exists(file_path):
            os.remove(file_path)
        serializer.delete()
