from .models import ApiLog
from rest_framework import serializers

class ApiLogserializer(serializers.ModelSerializer):
    class Meta:
        model=ApiLog
        fields= "__all__"