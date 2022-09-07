from rest_framework import serializers
from rest_framework.serializers import ValidationError

from .models import Diary

from argon2 import PasswordHasher


class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        exclude = ['update_date']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        if password is not None:
            password = PasswordHasher().hash(password)
        return Diary.objects.create(password=password, **validated_data)


class DiaryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    # def update(self, instance, pk, validated_data):
    #     password = validated_data.pop('password')
    #     pk = self.instance.pk
    #     diary = Diary.objects.get(pk=pk)
    #     diary_pw = diary.password
    #
    #     try:
    #        PasswordHasher().verify(diary_pw, password)
    #     except:
    #         msg = "비밀번호가 맞지 않거나 업데이트 할 수 없습니다."
    #         raise ValidationError(msg)
    #
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)