from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import FileSystemStorage

from apps.api.models import UploadedFile


class UploadedFileViewTest(TestCase):

    def test_upload_file_csv(self):
        """
        Test the upload file functionality for a CSV file.

        This test case creates a simple uploaded file with the content type of "text/csv".
        It then sends a POST request to the "/api/file/" endpoint with the uploaded file.
        The test asserts that:
        - The number of UploadedFile objects in the database is 1.
        - The file exists in the file system.
        - The response status code is 201.

        Parameters:
            self (TestCase): The test case instance.

        Returns:
            None
        """
        content = {"name": "test_file.csv", "type": "text/csv"}
        file = SimpleUploadedFile(
            content["name"], b"file_content", content_type=content["type"]
        )
        response = self.client.post("/api/file/", {"file": file})

        self.assertEqual(UploadedFile.objects.count(), 1)
        self.assertEqual(FileSystemStorage().exists(content["name"]), True)
        self.assertEqual(response.status_code, 201)

        FileSystemStorage().delete(content["name"])

    def test_upload_file_xls(self):
        """
        Test the upload file functionality for an Excel file.

        This test case creates a simple uploaded file with the content type of "application/vnd.ms-excel".
        It then sends a POST request to the "/api/file/" endpoint with the uploaded file.
        The test asserts that:
        - The number of UploadedFile objects in the database is 1.
        - The file exists in the file system.
        - The response status code is 201.

        Parameters:
            self (TestCase): The test case instance.

        Returns:
            None
        """
        content = {"name": "test_file.xls", "type": "application/vnd.ms-excel"}
        file = SimpleUploadedFile(
            content["name"], b"file_content", content_type=content["type"]
        )
        response = self.client.post("/api/file/", {"file": file})

        self.assertEqual(UploadedFile.objects.count(), 1)
        self.assertEqual(FileSystemStorage().exists(content["name"]), True)
        self.assertEqual(response.status_code, 201)

        FileSystemStorage().delete(content["name"])

    def test_upload_file_xlsx(self):
        """
        Test the upload file functionality for an Excel 2007+ file.

        This test case creates a simple uploaded file with the content type of "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet".
        It then sends a POST request to the "/api/file/" endpoint with the uploaded file.
        The test asserts that:
        - The number of UploadedFile objects in the database is 1.
        - The file exists in the file system.
        - The response status code is 201.

        Parameters:
            self (TestCase): The test case instance.

        Returns:
            None
        """
        content = {
            "name": "test_file.xlsx",
            "type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        }
        file = SimpleUploadedFile(
            content["name"], b"file_content", content_type=content["type"]
        )
        response = self.client.post("/api/file/", {"file": file})

        self.assertEqual(UploadedFile.objects.count(), 1)
        self.assertEqual(FileSystemStorage().exists(content["name"]), True)
        self.assertEqual(response.status_code, 201)

        FileSystemStorage().delete(content["name"])

    def test_upload_file_with_wrong_content_type(self):
        """
        Test the upload file functionality with a wrong content type.

        This test case creates a simple uploaded file with the content type of "text/plain" which is not allowed.
        It then sends a POST request to the "/api/file/" endpoint with the uploaded file.
        The test asserts that the response status code is 400.

        Parameters:
            self (TestCase): The test case instance.

        Returns:
            None
        """
        content = {"name": "test_file.txt", "type": "text/plain"}
        file = SimpleUploadedFile(
            content["name"], b"file_content", content_type=content["type"]
        )
        response = self.client.post("/api/file/", {"file": file})

        self.assertEqual(response.status_code, 400)

    def test_destroy_uploaded_file(self):
        """
        Test the functionality of deleting an uploaded file.

        This test case creates a simple uploaded file with an allowed content type.
        It sends a POST request to the "/api/file/" endpoint with the uploaded file.
        It then retrieves the first uploaded file from the database and sends a DELETE request to the "/api/file/{id}/" endpoint,
        where {id} is the ID of the uploaded file.
        The test asserts that:
        - The number of UploadedFile objects in the database is 0.
        - The file does not exist in the file system.
        - The response status code is 204.

        Parameters:
            self (TestCase): The test case instance.

        Returns:
            None
        """
        content = {"name": "test_deleted_file.csv", "type": "text/csv"}
        file = SimpleUploadedFile(
            content["name"], b"file_content", content_type=content["type"]
        )
        self.client.post("/api/file/", {"file": file})

        uploaded_file = UploadedFile.objects.first()
        response = self.client.delete(
            "/api/file/%s/" % uploaded_file.id,
        )
        self.assertEqual(UploadedFile.objects.count(), 0)
        self.assertEqual(FileSystemStorage().exists(content["name"]), False)
        self.assertEqual(response.status_code, 204)
