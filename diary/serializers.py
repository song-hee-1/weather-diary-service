from rest_framework import serializers
from rest_framework.serializers import ValidationError

from .models import Diary

import bcrypt


class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        exclude = ['update_date']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)

        if password is not None:
            encode_password = password.encode('utf-8')  # 입력받은 password는 문자형(유니코드)기 때문에 hash를 위해 바이트형으로 인코딩
            encrypt_password = bcrypt.hashpw(encode_password, bcrypt.gensalt())
            decode_password = encrypt_password.decode('utf-8')  # DB 필드는 문자형(유니코드)이므로 다시 유니코드로 디코딩하여 저장

        return Diary.objects.create(password=decode_password, **validated_data)


class DiaryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        password = password.encode('utf-8')  # checkpw 이용을 위한 인코딩
        diary_password = instance.password.encode('utf-8')

        if not bcrypt.checkpw(password, diary_password):
            msg = "비밀번호가 맞지 않거나 업데이트 할 수 없습니다."
            raise ValidationError(msg)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class DiaryDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ('password',)


    def validate_password(self, value):
        if not value:
            msg = "비밀번호를 입력해주세요."
            raise ValidationError(msg)
        return value


    # Update method는 왜 유효성 검증이 안되는 것인가
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        if not password:
            msg = "비밀번호를 입력해주세요."
            raise ValidationError(msg)

        password = password.encode('utf-8')
        diary_password = instance.password.encode('utf-8')

        if not bcrypt.checkpw(password, diary_password):
            msg = "비밀번호가 맞지 않거나 삭제 할 수 없습니다."
            raise ValidationError(msg)

        instance.save()
        return instance
