from django.core.exceptions import ValidationError


def PasswordMinimumLengthValidator(value):
    """비밀번호가 min_legnth 미만이면 Validation Error를 일으킨다."""

    min_length = 6

    if len(value) < min_length:
        msg = f"이 비밀번호는 {len(value)}자리로 너무 짧습니다. 비밀번호는 적어도 {min_length}자리 이상이어야 합니다."
        raise ValidationError(msg)


def PasswordNumbericValidator(value):
    """비밀번호에 숫자가 포함되지 않으면 Validation Error를 일으킨다."""

    if value.isalpha():
        msg = "이 비밀번호는 문자로만 이루어져 있습니다. 비밀번호는 적어도 숫자를 1개 이상 포함해야 합니다."
        raise ValidationError(msg)
