from datetime import (
    datetime,
    timedelta,
    timezone
)

from jose import jwt
from jose import JWTError


SECRET_KEY = "miriamariliacunha"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_DAYS = 7


def create_access_token(
        payload: dict
):

    data = payload.copy()

    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        days=ACCESS_TOKEN_EXPIRE_DAYS
    )

    data.update(
        {"exp": expire}
    )

    token = jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def decode_token(
        token:str
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        return None