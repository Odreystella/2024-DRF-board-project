from rest_framework.exceptions import APIException


class EmailRequiredException(APIException):
    status_code = 400
    default_code = 'EmailRequired'
    default_detail = '이메일은 필수로 입력해주세요.'


class PasswordNotValidException(APIException):
    status_code = 400
    default_code = 'PasswordNotValid'
    default_detail = '비밀번호는 8자 이상, 소문자, 대문자, 특수문자 각 1자리 이상 포함해야 합니다.'


class UserNotFoundException(APIException):
    status_code = 404
    default_code = 'UserNotFound'
    default_detail = '해당 이메일의 유저가 존재하지 않습니다.'


class PasswordNotMatchedException(APIException):
    status_code = 400
    default_code = 'PasswordNotMatched'
    default_detail = '인증에 실패하였습니다.'


class EmptyInputException(APIException):
    status_code = 400
    default_code = 'EmptyInput'
    default_detail = '빈값은 허용되지 않습니다.'


class TemporaryRedirectException(APIException):
    status_code = 307
    default_code = 'TemporaryRedirect'
    default_detail = '다시 로그인해주세요.'


class IsNotMeException(APIException):
    status_code = 403
    default_code = 'IsNotMe'
    default_detail = '본인이 아닙니다.'


class InvalidJWTTokenException(APIException):
    status_code = 401
    default_code = 'InvalidJWTToken'
    default_detail = '유효한 토큰이 아닙니다.'