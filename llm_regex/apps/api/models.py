from django.db import models
from django.core.files.storage import FileSystemStorage


class UploadedFile(models.Model):
    file = models.FileField()
    uploaded_on = models.DateTimeField(auto_now_add=True)
    content_type = models.CharField(max_length=100, blank=True)

    def delete(self, *args, **kwargs):
        FileSystemStorage().delete(self.file.name)
        super().delete(*args, **kwargs)

    def __str__(self):
        return str(self.file.name)


class NlpQuery(models.Model):
    query = models.CharField(max_length=500)
    same_file = models.BooleanField(default=False)

    def __str__(self):
        return self.query
