from rest_framework.exceptions import APIException


class PostNotFoundException(APIException):
    status_code = 404
    default_code = 'PostNotFound'
    default_detail = '해당 포스트가 존재하지 않습니다.'