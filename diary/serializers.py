from rest_framework import serializers

from .models import Diary


class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        exclude = ['update_date']
        extra_kwargs = {'password': {'write_only': True}}


class DiaryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        extra_kwargs = {'password': {'write_only': True}}
