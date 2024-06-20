from rest_framework.exceptions import APIException
from rest_framework import status


class EmailRequiredException(APIException):
    status_code = 400
    default_code = 'EmailRequired'
    default_detail = '이메일은 필수로 입력해주세요.'