from django.db import models


class UploadedFile(models.Model):
    file = models.FileField()

    def __str__(self):
        """
        Return a string representation of the object.

        This method returns a string representation of the object by calling the `name` attribute of the `file` field.

        Returns:
            str: The name of the file.
        """
        return str(self.file.name)
