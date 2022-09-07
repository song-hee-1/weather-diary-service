from rest_framework import viewsets

from .models import Diary
from .serializers import DiarySerializer, DiaryDetailSerializer
from .pagination import DiaryPagination


class DiaryViewSet(viewsets.ModelViewSet):
    queryset = Diary.objects.all()
    pagination_class = DiaryPagination

    def get_serializer_class(self):
        if self.action in ("list", "create"):
            return DiarySerializer
        if self.action in ("retrieve", "update", "partial_update"):
            return DiaryDetailSerializer
        return DiaryDetailSerializer
