from datetime import datetime, timedelta
from token_store import load_tokens


def is_token_expired(token_time_str: str, max_age_minutes: int) -> bool:
    """
    Checks whether a token has expired or not.
    :param token_time_str: Time to receive token as a string (ISO format)
    :param max_age_minutes: Token valid life in minutes
    :return: True if the token has expired, False otherwise
    """

    try:
        token_time = datetime.fromisoformat(token_time_str)
    except Exception:
        return True

    return datetime.now() - token_time > timedelta(minutes=max_age_minutes)


def should_refresh_token(email: str) -> bool:
    """
    Checks whether a token refresh is required for a specific user.
    :param email: User's email address
    :return: True if the access token has expired, False otherwise.
    """

    tokens = load_tokens(email)
    if not tokens or "access_token_time" not in tokens:
        return True
    return is_token_expired(tokens["access_token_time"], 2)


def is_refresh_token_valid(email: str) -> bool:
    """
    Checks whether the refresh token is still valid or not.
    :param email: User's email address
    :return: True if valid, False if expired
    """

    tokens = load_tokens(email)
    if not tokens or "refresh_token" not in tokens:
        return False
    return not is_token_expired(tokens["refresh_token_time"], 4)
