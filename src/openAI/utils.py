# import jwt
# import os
# from dotenv import load_dotenv
# import time

# dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
# load_dotenv(dotenv_path)

# jwt_secret = os.getenv('JWT_SECRET')


# def decodeJWT(token: str) -> dict:
#   try:
#     decoded_token = jwt.decode(token, jwt_secret, algorithms=["HS256"], options={"verify_aud": False})
#     return decoded_token if decoded_token["exp"] >= time.time() else None
#   except Exception as e:
#       return {"error": str(e)}
