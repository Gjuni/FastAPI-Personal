import re

# id는 반드시 4자 이상
userNameRegex = re.compile(r"^[a-zA-Z0-9]{4,}$")

# pw는 8자리 이상 특수문자, 숫자, 알파벳 반드시 포함
passwordRegex = re.compile(r"^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")


def userNameRegexCheck(value: str) -> bool:
    return bool(userNameRegex.fullmatch(value or ""))

def passwordRegexCheck(value: str) -> bool:
    return bool(passwordRegex.fullmatch(value or ""))