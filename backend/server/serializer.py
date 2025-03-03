from rest_framework import serializers
from server import models


class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Server

        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category

        fields = "__all__"
