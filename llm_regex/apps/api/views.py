from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError

from .models import UploadedFile
from .serializers import UploadedFileSerializer


class UploadedFileViewSet(ModelViewSet):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer

    def perform_create(self, serializer):
        """
        Perform the creation of a new object using the given serializer.

        Args:
            serializer (Serializer): The serializer instance containing the data for the new object.

        Raises:
            ValidationError: If the content type of the file in the serializer data is not allowed.

        Returns:
            None
        """
        allowed_content_types = [
            "text/csv",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/vnd.ms-excel",
        ]

        if serializer.validated_data["file"].content_type not in allowed_content_types:
            raise ValidationError(
                {"message": "Unsupported file type. Please upload a CSV or Excel file."}
            )

        serializer.save()

    def perform_destroy(self, serializer):
        """
        Deletes a file associated with the given serializer and removes it from the file system.

        Parameters:
            serializer (Serializer): The serializer object containing the file to be deleted.

        Returns:
            None
        """
        if FileSystemStorage().exists(serializer.file.name):
            FileSystemStorage().delete(serializer.file.name)
        serializer.delete()
