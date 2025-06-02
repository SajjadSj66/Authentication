
# FastAPI Auth Client

This is a simple FastAPI client that connects to a centralized authentication system using JWT (access and refresh tokens). It supports user registration, login, protected route access, automatic token refresh, and local token storage.

## ✨ Features

- User registration to a central auth system
- User login with access and refresh token retrieval
- Local storage of tokens in a JSON file
- Access to protected resources using access tokens
- Automatic refresh of expired tokens
- Basic error handling for token failures

## 🔧 Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [HTTPX](https://www.python-httpx.org/)
- [Uvicorn](https://www.uvicorn.org/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

## ⚙️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/fastapi-auth-client.git
cd fastapi-auth-client
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables

Create a `.env` file and add your central auth API base URL:

```
AUTH_API_KEY=https://auth-central-challange.vercel.app
```

### 4. Run the App
```bash
uvicorn main:app --reload
```

## 🧪 API Usage

### 🔹 Register a New User
`POST /register`  
Request Body (JSON):  
```json
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

### 🔹 Login
`POST /login`  
Request Body (JSON):  
```json
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

### 🔹 Access Protected Route
`GET /protected-data`  
Requires valid `access_token`.

### 🔹 Refresh Token
Token refresh is handled automatically if the access token is expired.

## 📂 Project Structure

```
.
├── main.py               # FastAPI app entry point
├── auth.py               # Auth-related functions (register/login/refresh)
├── token_store.py        # Token storage/retrieval
├── .env                  # Environment variables
├── tokens.json           # Locally stored tokens (runtime-generated)
└── requirements.txt      # Python dependencies
```

## 📌 Notes

- Tokens are stored in `tokens.json` per user email.
- Access tokens expire in 2 minutes; refresh tokens expire in 4 minutes.

## 📤 Contributing

Feel free to open issues or submit pull requests. Contributions are welcome!

## 📜 License

This project is licensed under the MIT License.
