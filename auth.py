from datetime import timedelta
import httpx
from dotenv import load_dotenv
from token_store import *

load_dotenv()

AUTH_API_BASE = os.getenv("AUTH_API_KEY")


async def register_user(email: str, password: str):
    """
    In this section, the user registers by
    entering their email and password.
    """
    url = f"{AUTH_API_BASE}/register"
    data = {
        "email": email,
        "password": password,
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=data)
        except httpx.RequestError as e:
            return {
                "success": False,
                "message": "Connection error",
                "detail": str(e)
            }

    if response.status_code == 201:
        return {"success": True, "message": "Register successful!"}
    else:
        return {
            "success": False,
            "message": "Register failed",
            "status_code": response.status_code,
            "detail": response.text
        }


async def login_user(email: str, password: str):
    """
     In this section, the user logs in using their email and password to
     generate an access token and refresh token
     for each user and store them as JSON.
    """
    url = f"{AUTH_API_BASE}/login"
    data = {"username": email, "password": password}
    print("Sending login payload:", data)

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, data=data, headers=headers)
        except httpx.RequestError as e:
            return {
                "success": False,
                "message": "Connection error",
                "detail": str(e)
            }

    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens.get("access_token")
        refresh_token = tokens.get("refresh_token")
        save_tokens(email, access_token, refresh_token)
        return {
            "success": True,
            "message": "Login successful!",
            "tokens": tokens
        }
    else:
        print("Login response:", response.status_code, response.text)

        return {
            "success": False,
            "message": "Login failed",
            "status_code": response.status_code,
            "detail": response.text,
        }


async def get_protected_data(email: str):
    """
    This code manages the tokens and if the access token
    expires based on time, it sends a refresh token and
    gets and stores the new access token.
    """
    tokens = load_tokens(email)
    if not tokens:
        return {"message": "No tokens found!"}

    access_token = tokens.get("access_token")
    access_token_time = tokens.get("access_token_time")

    # Checking access token expiration
    if access_token_time:
        access_time = datetime.fromisoformat(access_token_time)
        if datetime.now() - access_time > timedelta(minutes=2):
            refreshed = await refresh_access_token(email)
            if not refreshed.get("access_token"):
                return {"message": "Refresh token expired!", "detail": refreshed}
            access_token = refreshed["access_token"]

    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    url = f"{AUTH_API_BASE}/protected"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
    except httpx.RequestError as e:
        return {"message": "Connection error", "detail": str(e)}

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        # In case of a 401 error, try again with refresh.
        refreshed = await refresh_access_token(email)
        if not refreshed.get("access_token"):
            return {"message": "Access token expired or invalid. Try refreshing token."}

        access_token = refreshed["access_token"]
        headers["Authorization"] = f"Bearer {access_token}"

        async with httpx.AsyncClient() as client:
            retry_response = await client.get(url, headers=headers)

        if retry_response.status_code == 200:
            return retry_response.json()
        else:
            return {
                "message": "Retry after refresh failed",
                "status_code": retry_response.status_code,
                "detail": retry_response.text
            }
    else:
        return {
            "message": "Failed to get protected data",
            "status_code": response.status_code,
            "detail": response.text}


async def refresh_access_token(email: str):
    """
    Get a new token using a refresh token.
    """
    tokens = load_tokens(email)
    if not tokens:
        return {"message": "No refresh token found for this user!"}

    refresh_token = tokens.get("refresh_token")
    if not refresh_token:
        return {"message": "Refresh token not available!"}

    url = f"{AUTH_API_BASE}/refresh"
    data = {"refresh_token": refresh_token}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data)
    except httpx.RequestError as e:
        return {"message": "Connection error", "detail": str(e)}

    if response.status_code == 200:
        new_tokens = response.json()
        access_token = new_tokens.get("access_token")
        refresh_token = new_tokens.get("refresh_token")
        save_tokens(email, access_token, refresh_token)
        return {"message": "Access token updated successfully!", "tokens": new_tokens}
    else:
        return {
            "message": "Failed to refresh access token",
            "status_code": response.status_code,
            "detail": response.text}
