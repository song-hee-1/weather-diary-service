from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from diary.models import Diary

import bcrypt

"""
- 게시글
    1. 본문(content)
        1) 본문이 200자 초과할 때 : 실패
        2) 본문이 200자 초과하지 않을 때 : 성공
        3) 본문에 이모지 포함되어 있을 때 : 성공

    2. 제목(title)
        1) 제목이 20자 초과할 때 : 실패
        2) 제목이 20자 초과하지 않을 때 : 성공
        3) 제목에 이모지 포함되어 있을 때 : 성공

    3. create시
        1) 비밀번호가 6자 이하일 때 : 실패
        2) 비밀번호가 6자 이상일 때 : 성공
        3) 비밀번호가 문자로만 이루어져 있을 때 : 실패
        4) 비밀번호가 1개 이상의 숫자로 이루어져 있을 때 : 성공
        5) 비밀번호가 암호화 되어 있는지 확인

    4. update시
        1) 비밀번호가 틀렸을 때 : 실패
        2) 비밀번호가 맞을 때 : 성공

    5. delete시
        1) 비밀번호가 틀렸을 때 : 실패
        2) 비밀번호가 맞을 때 : 성공
"""


class DiaryTitleTestCase(APITestCase):
    def test_create_fail_title_more_20_char(self):
        data = {
            "title": "제목이 20자를 초과할 때 생성되지 않는 테스트중입니다. 이 글은 총 46자입니다.",
            "content": "본문",
            "password": "1aaaaa",
            "nickname": "핑핑"
        }
        response = self.client.post(reverse('diary-list'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_success_title_less_20_char(self):
        data = {
            "title": "제목이 20자 이하 테스트중입니다.",
            "content": "본문",
            "password": "1aaaaa",
            "nickname": "핑핑"
        }
        response = self.client.post(reverse('diary-list'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_success_emoji(self):
        data = {
            "title": "이모지 테스트😀",
            "content": "본문",
            "password": "1aaaaa",
            "nickname": "핑핑"
        }
        response = self.client.post(reverse('diary-list'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class DiaryContentTestCase(APITestCase):
    def test_create_fail_content_more_200_char(self):
        data = {
            "title": "본문이 200자 초과할 때 테스트",
            "content": "본문이 200자 초과일 때는 게시글이 등록되지 않는지 확인하는 테스트입니다." * 5,
            "password": "1aaaaa",
            "nickname": "핑핑"
        }
        response = self.client.post(reverse('diary-list'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_success_title_less_20_char(self):
        data = {
            "title": "본문 200자 미만일 때 테스트",
            "content": "본문이 200자를 초과하지 않을 때에는 게시글이 정상적으로 등록되는지 확인하는 테스트입니다.",
            "password": "1aaaaa",
            "nickname": "핑핑"
        }
        response = self.client.post(reverse('diary-list'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_success_emoji(self):
        data = {
            "title": "이모지 테스트",
            "content": "본문에 이모지가 포함되어 있을 때 게시글이 등록되는지 확인하는 테스트입니다. 😀",
            "password": "1aaaaa",
            "nickname": "핑핑"
        }
        response = self.client.post(reverse('diary-list'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class DiaryCreateTest(APITestCase):
    def test_create_fail_password_less_6(self):
        data = {
            "title": "비밀번호 테스트",
            "content": "비밀번호가 6자 미만일 때 생성되지 않는 테스트",
            "password": "1aaaa",
            "nickname": "핑핑"
        }
        response = self.client.post(reverse('diary-list'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_success_password_more_6(self):
        data = {
            "title": "비밀번호 테스트",
            "content": "비밀번호가 6자 미만일 때 생성되지 않는 테스트",
            "password": "1aaaaa",
            "nickname": "핑핑"
        }
        response = self.client.post(reverse('diary-list'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_fail_password_isalpha(self):
        data = {
            "title": "비밀번호 테스트",
            "content": "비밀번호가 문자로만 이루어져 있을 때 생성되지 않는 테스트",
            "password": "aaaaaa",
            "nickname": "핑핑"
        }
        response = self.client.post(reverse('diary-list'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_success_password_not_isalpha(self):
        data = {
            "title": "비밀번호 테스트",
            "content": "비밀번호가 문자로만 이루어져 있지 않고 1개 이상의 숫자를 포함할 때 생성되는 테스트",
            "password": "1aaaaa",
            "nickname": "핑핑"
        }
        response = self.client.post(reverse('diary-list'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_password_encrypt(self):
        encode_password = "1aaaaa".encode('utf-8')
        encrypt_password = bcrypt.hashpw(encode_password, bcrypt.gensalt())
        decode_password = encrypt_password.decode('utf-8')
        data = {
            "title": "비밀번호 암호화 테스트",
            "content": "비밀번호가 암호화 됐는지 확인하는 테스트",
            "password": decode_password,
            "nickname": "핑핑"
        }
        response = self.client.post(reverse('diary-list'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class DiaryUpdateTest(APITestCase):
    def setUp(self):
        encode_password = "1aaaaa".encode('utf-8')
        encrypt_password = bcrypt.hashpw(encode_password, bcrypt.gensalt())
        decode_password = encrypt_password.decode('utf-8')
        self.diary = Diary.objects.create(
            title= "제목 테스트", content= "본문 테스트", password= decode_password, nickname= "핑핑"
        )

    def test_update_fail_password_not_match(self):
        update_data = {
            "title": "제목 수정 테스트",
            "content": "본문 수정 테스트",
            "password": "2aaaaa",
            "nickname": "핑핑"
        }
        response = self.client.put(reverse('diary-detail', kwargs={'pk': 1}), update_data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_success_password_match(self):
        update_data = {
            "title": "제목 수정 테스트",
            "content": "본문 수정 테스트",
            "password": "1aaaaa",
            "nickname": "핑핑"
        }
        response = self.client.put(reverse('diary-detail', kwargs={'pk': 1}), update_data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)


class DiaryDeleteTest(APITestCase):
    def setUp(self):
        encode_password = "1aaaaa".encode('utf-8')
        encrypt_password = bcrypt.hashpw(encode_password, bcrypt.gensalt())
        decode_password = encrypt_password.decode('utf-8')
        self.diary = Diary.objects.create(
            title= "제목 테스트", content= "본문 테스트", password=decode_password, nickname= "핑핑"
        )

    def test_delete_fail_password_not_match(self):
        data = {"password": "2aaaaa"}
        response = self.client.post(reverse('diary-delete', kwargs={'pk': 1}), data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_success_password_match(self):
        data = {"password": "1aaaaa"}
        response = self.client.post(reverse('diary-delete', kwargs={'pk': 1}), data)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
