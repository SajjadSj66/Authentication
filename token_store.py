import json
import os
from datetime import datetime

TOKEN_FILE = 'tokens.json'


def save_tokens(email, access_token, refresh_token):
    """
    It stores the email, access token, refresh token, and date in the tokens.json file.
    """
    tokens = load_all_tokens()
    tokens[email] = {
        "email": email,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "access_token_time": datetime.now().isoformat(),
        "refresh_token_time": datetime.now().isoformat(),
    }
    with open(TOKEN_FILE, 'w') as f:
        json.dump(tokens, f, indent=4)

    # Save the last login user email.
    with open("last_user.txt", "w") as f:
        f.write(email)


def get_last_logged_email():
    """
    Returns the last email.
    """
    try:
        with open(TOKEN_FILE, 'r') as f:
            data = json.load(f)
            if not data:
                return None
            last_email = list(data.keys())[-1]
            return last_email
    except Exception as e:
        return None


# Loads the tokens.
def load_tokens(email):
    tokens = load_all_tokens()
    return tokens.get(email)


# Loads the all tokens.
def load_all_tokens():
    if not os.path.exists(TOKEN_FILE):
        return {}

    try:
        with open(TOKEN_FILE, 'r') as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except Exception as e:
        print(f"Error loading tokens: {e}")
        return {}
