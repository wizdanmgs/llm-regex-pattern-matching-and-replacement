import pandas as pd

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status

from .models import UploadedFile, NlpQuery
from .serializers import UploadedFileSerializer, NlpQuerySerializer


class UploadedFileViewSet(ModelViewSet):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new instance of the `UploadedFile` model based on the provided data.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The HTTP response containing the serialized data and the table in JSON format if the file is valid,
                      or the serializer errors if the file is not valid.

        Notes:
            - The function first checks if the provided data is valid by using the serializer.
            - If the data is valid, it retrieves the file from the serializer's validated data.
            - It then checks if the file's content type is one of the allowed content types. If not, it returns a 400
              Bad Request response with an error message.
            - If the file's content type is "text/csv", it reads the file using `pd.read_csv()`. Otherwise, it reads the
              file using `pd.read_excel()` with the "openpyxl" engine.
            - It then converts the DataFrame to JSON format with the "records" orientation.
            - Finally, it saves the serializer and returns a 201 Created response with the serialized data and the table
              in JSON format.

        """
        serializer = self.serializer_class(data=request.data)

        allowed_content_types = [
            "text/csv",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/vnd.ms-excel",
        ]

        if serializer.is_valid():
            file = serializer.validated_data["file"]
            if file.content_type not in allowed_content_types:
                return Response(
                    {
                        "status": 400,
                        "message": "Unsupported file type. Please upload a CSV or Excel file.",
                        "data": None,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if file.content_type == "text/csv":
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file, engine="openpyxl")

            json_data = df.to_json(orient="records")

            serializer.save()

            return Response(
                {
                    "status": 200,
                    "message": "File uploaded successfully.",
                    "data": {"serializer": serializer.data, "table": json_data},
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {
                "status": 400,
                "message": "Invalid file. Please upload a CSV or Excel file.",
                "data": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

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


class NlpQueryViewSet(ModelViewSet):
    queryset = NlpQuery.objects.all()
    serializer_class = NlpQuerySerializer

    def perform_create(self, serializer):
        # TODO: connect to LLM and perform NLP query
        raise ValidationError({"message": "NLP queries cannot be created directly."})
