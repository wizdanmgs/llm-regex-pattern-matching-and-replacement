from django.urls import path
from .views import UploadedFileView

urlpatterns = [
    path("api/file/", UploadedFileView.as_view(), name="file"),
]
