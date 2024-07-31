from django.db import models


class UploadedFile(models.Model):
    file = models.FileField()

    def __str__(self):
        return str(self.file.name)


class NlpQuery(models.Model):
    query = models.CharField(max_length=500)

    def __str__(self):
        return self.query
