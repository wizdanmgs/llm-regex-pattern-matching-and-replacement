from django.shortcuts import render
from apps.api.models import UploadedFile, NlpQuery


def index(request):
    # Clean database
    uploaded_files = UploadedFile.objects.all()
    for file in uploaded_files:
        file.delete()
    NlpQuery.objects.all().delete()

    return render(request, "frontend/index.html")
