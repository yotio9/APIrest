import base64
import binascii
import hashlib
import hmac
import json
import math
import re
import time
from datetime import datetime, timedelta, timezone
from typing import Annotated, Any

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.setting import settings

_bearer_scheme = HTTPBearer(auto_error=False)
_SEGMENT_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")
_ACCESS_TOKEN_LIFETIME = timedelta(minutes=30)
_MAX_TOKEN_LENGTH = 4096


class InvalidTokenError(ValueError):
    pass


def _signing_key() -> bytes:
    if not settings.JWT_SECRET:
        raise RuntimeError("JWT_SECRET must not be empty")
    return settings.JWT_SECRET.encode("utf-8")


def _encode_segment(value: dict[str, Any]) -> str:
    serialized = json.dumps(value, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return base64.urlsafe_b64encode(serialized).rstrip(b"=").decode("ascii")


def _decode_segment(segment: str) -> Any:
    if not _SEGMENT_PATTERN.fullmatch(segment):
        raise InvalidTokenError("Malformed token")
    padded_segment = segment + "=" * (-len(segment) % 4)
    try:
        decoded = base64.b64decode(padded_segment, altchars=b"-_", validate=True)
        return json.loads(decoded)
    except (
        binascii.Error,
        UnicodeDecodeError,
        json.JSONDecodeError,
        RecursionError,
    ) as error:
        raise InvalidTokenError("Malformed token") from error


def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
) -> str:
    if not subject:
        raise ValueError("Token subject must not be empty")

    expires_at = datetime.now(timezone.utc) + (
        _ACCESS_TOKEN_LIFETIME if expires_delta is None else expires_delta
    )
    header = _encode_segment({"alg": "HS256", "typ": "JWT"})
    payload = _encode_segment({"sub": subject, "exp": int(expires_at.timestamp())})
    signing_input = f"{header}.{payload}".encode("ascii")
    signature = hmac.new(_signing_key(), signing_input, hashlib.sha256).digest()
    encoded_signature = base64.urlsafe_b64encode(signature).rstrip(b"=").decode("ascii")
    return f"{header}.{payload}.{encoded_signature}"


def decode_access_token(token: str) -> dict[str, Any]:
    if len(token) > _MAX_TOKEN_LENGTH:
        raise InvalidTokenError("Token is too large")

    try:
        header_segment, payload_segment, signature_segment = token.split(".")
    except ValueError as error:
        raise InvalidTokenError("Malformed token") from error

    header = _decode_segment(header_segment)
    if not isinstance(header, dict) or header.get("alg") != "HS256":
        raise InvalidTokenError("Unsupported token algorithm")

    if not _SEGMENT_PATTERN.fullmatch(signature_segment):
        raise InvalidTokenError("Malformed token")
    padded_signature = signature_segment + "=" * (-len(signature_segment) % 4)
    try:
        signature = base64.b64decode(padded_signature, altchars=b"-_", validate=True)
    except binascii.Error as error:
        raise InvalidTokenError("Malformed token") from error

    signing_input = f"{header_segment}.{payload_segment}".encode("ascii")
    expected_signature = hmac.new(_signing_key(), signing_input, hashlib.sha256).digest()
    if not hmac.compare_digest(signature, expected_signature):
        raise InvalidTokenError("Invalid token signature")

    payload = _decode_segment(payload_segment)
    if not isinstance(payload, dict):
        raise InvalidTokenError("Malformed token payload")

    subject = payload.get("sub")
    expiration = payload.get("exp")
    if not isinstance(subject, str) or not subject:
        raise InvalidTokenError("Token subject is missing")
    if (
        isinstance(expiration, bool)
        or not isinstance(expiration, (int, float))
        or not math.isfinite(expiration)
        or expiration <= time.time()
    ):
        raise InvalidTokenError("Token is expired or has no valid expiration")

    return payload


async def get_current_user_id(
    request: Request,
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(_bearer_scheme),
    ],
) -> int:
    if credentials is None:
        token = request.cookies.get("access_token")
        if token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=(
                    "Authentication token missing. Log in via /auth/connection/ "
                    "or send Authorization: Bearer <access_token>."
                ),
                headers={"WWW-Authenticate": "Bearer"},
            )
    elif credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme. Use Bearer.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        token = credentials.credentials

    try:
        payload = decode_access_token(token)
        user_id = int(payload["sub"])
    except (InvalidTokenError, ValueError) as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token invalid or expired. Log in again via /auth/connection/.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from error

    if user_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token invalid. Log in again via /auth/connection/.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id