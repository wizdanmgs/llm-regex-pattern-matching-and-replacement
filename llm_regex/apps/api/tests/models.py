from django.test import TestCase
from apps.api.models import UploadedFile


class UploadedFileModelTest(TestCase):
    def test_str(self):
        """
        Test the __str__ method of the UploadedFile model.

        This test case creates an instance of the UploadedFile model with a file name
        of "test_file.csv" and checks if the __str__ method returns the same file name.

        Parameters:
            self (TestCase): The test case instance.

        Returns:
            None
        """
        uploaded_file = UploadedFile.objects.create(file="test_file.csv")
        self.assertEqual(str(uploaded_file), uploaded_file.file.name)
