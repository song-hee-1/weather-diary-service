from django.db import models
from .validation import PasswordMinimumLengthValidator, PasswordNumbericValidator


class Diary(models.Model):
    diary_id = models.AutoField(primary_key=True, verbose_name="일기_id")
    title = models.CharField(max_length=20, verbose_name="제목")
    content = models.CharField(max_length=200, verbose_name="본문")
    password = models.CharField(max_length=120, verbose_name="비밀번호",
                                validators=[PasswordMinimumLengthValidator, PasswordNumbericValidator])
    # 암호화를 위한 큰 길이 지정 및 비밀번호 유효성 검증 validator 추가
    nickname = models.CharField(max_length=10, verbose_name="작성자별명")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="생성날짜")
    update_date = models.DateTimeField(auto_now=True, verbose_name="수정날짜")

    class Meta:
        verbose_name = "일기"
        verbose_name_plural = "일 목록"
        db_table = 'diary'

    def __str__(self):
        return self.title
