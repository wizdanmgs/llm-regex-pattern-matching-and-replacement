from rest_framework import serializers

from .models import UploadedFile, NlpQuery


class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = "__all__"


class NlpQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = NlpQuery
        fields = "__all__"
