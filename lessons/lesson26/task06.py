from datetime import datetime, timezone

my_token_analyze_from_jwt_dot_io = {
    "token_type": "access",
    "exp": 1787914496,
    "iat": 1787914196,
    "jti": "254f77f4e4704c009787295f4acf7acd",
    "user_id": "3",
}

check = int(
    (
        my_token_analyze_from_jwt_dot_io["exp"]
        - my_token_analyze_from_jwt_dot_io["iat"]
    )
    / 60
)

print(f"Expiration time of my token in minutes: {check}")
