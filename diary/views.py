from rest_framework import viewsets

from .models import Diary
from .serializers import DiarySerializer, DiaryDetailSerializer


class DiaryViewSet(viewsets.ModelViewSet):
    queryset = Diary.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "create"):
            return DiarySerializer
        if self.action in ("retrieve", "update", "partial_update"):
            return DiaryDetailSerializer
        return DiaryDetailSerializer
