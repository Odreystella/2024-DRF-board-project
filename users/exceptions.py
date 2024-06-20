from rest_framework.exceptions import APIException
from rest_framework import status


class EmailRequiredException(APIException):
    status_code = 400
    default_code = 'EmailRequired'
    default_detail = '이메일은 필수로 입력해주세요.'


class PasswordNotValidException(APIException):
    status_code = 400
    default_code = 'PasswordNotValid'
    default_detail = '비밀번호는 8자 이상, 소문자, 대문자, 특수문자 각 1자리 이상 포함해야 합니다.'