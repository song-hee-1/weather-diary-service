from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Diary
from .serializers import DiarySerializer, DiaryDetailSerializer
from .pagination import DiaryPagination
from .utils import get_weather_info


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
