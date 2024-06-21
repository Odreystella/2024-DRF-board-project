import re

from users.exceptions import PasswordNotValidException


def validate_password(password):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).{8,}$'
    if not re.match(pattern, password):
        raise PasswordNotValidException
    return password