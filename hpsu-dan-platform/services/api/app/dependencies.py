from __future__ import annotations

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from .core.security import decode_access_token
from .db import User, find_user, get_session


bearer = HTTPBearer(auto_error=False)


def current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    session: Session = Depends(get_session),
) -> User:
    if credentials is None:
        raise HTTPException(status_code=401, detail="AUTH_REQUIRED")
    try:
        payload = decode_access_token(credentials.credentials)
    except InvalidTokenError as exc:
        raise HTTPException(status_code=401, detail="AUTH_TOKEN_INVALID") from exc
    user = find_user(session, payload.get("sub", ""))
    if user is None or not user.active:
        raise HTTPException(status_code=401, detail="AUTH_USER_INACTIVE")
    return user


def require_roles(*roles: str):
    def dependency(user: User = Depends(current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="AUTH_FORBIDDEN")
        return user

    return dependency

