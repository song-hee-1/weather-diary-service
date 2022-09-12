from rest_framework import viewsets, status
from rest_framework.response import Response
<<<<<<< HEAD
=======
from rest_framework.serializers import ValidationError
>>>>>>> main

from .models import Diary
from .serializers import DiarySerializer, DiaryDetailSerializer, DiaryDeleteSerializer
from .pagination import DiaryPagination
from .utils import get_weather_info

import bcrypt


class DiaryViewSet(viewsets.ModelViewSet):
    queryset = Diary.objects.all()
    pagination_class = DiaryPagination

    def get_serializer_class(self):
        if self.action in ("list", "create"):
            return DiarySerializer
        if self.action in ("retrieve", "update", "partial_update"):
            return DiaryDetailSerializer
        return DiaryDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        current_weather = get_weather_info(request)
        self.perform_create(serializer, current_weather)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, weather=None):
        serializer.save(weather=weather)

        if self.action == "destory":
            return DiaryDeleteSerializer
        return DiarySerializer

    def destroy(self, request, *args, **kwargs):
        # destory시 password 값을 받아오기 위해 update 로직 이용
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = DiaryDeleteSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # 유효성을 검증하지 않고 바로 삭제되는 버그 확인 (수정예정)
        instance.delete()
        response = {'성공적으로 삭제되었습니다.'}
        return Response(response, status=status.HTTP_204_NO_CONTENT)
