from rest_framework.pagination import CursorPagination


class DiaryPagination(CursorPagination):
    page_size = 20
    ordering = '-create_date'
