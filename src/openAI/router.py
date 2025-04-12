from typing import List
from fastapi import APIRouter

from src.openAI.models import ClientMessages
from src.openAI.BackendLogic import getOpenAIResponse

router = APIRouter()


# This route is used to get a response from OpenAI. It takes in a list of messages and a conversation_id.
@router.post("/api/response")
async def getAPIResponse(messages: List[ClientMessages], conversation_id, model: str):

    return getOpenAIResponse(
        messages=messages, conversation_id=conversation_id, model=model
    )


# @DeprecationWarning  # This is a test route. Do not use
# @router.post("/api/test/response")
# async def testParams(messages: List[ClientMessages], conversation_id: str, model: str):
#     return {"messages": messages, "conversationid": conversation_id, "model": model}


# @DeprecationWarning  # This is a test route. Do not use
# @router.post("/jwt")
# async def getDecodeJWT(request: Request):
#     body = await request.json()
#     token = body["token"]
#     decoded = decodeJWT(token)
#     return decoded


"""
This route is used to decode a JWT token. This is a test route to see how you can do it @ Robin.

For this to work you need to be signed into the Frontend. These tokens expire after 5 minutes I believe.

1. Log into frontend
2. Open the console right click->inspect->console
3. You should see something like this:
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsImtpZCI6ImQ3ZzY0Z3k5RlVGbTZ1YjMiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzA4NzUwNDMyLCJpYXQiOjE3MDg3NDY4MzIsImlzcyI6Imh0dHBzOi8va2N1eWRldGJwZWJpYnZpZWJxZncuc3VwYWJhc2UuY28vYXV0aC92MSIsInN1YiI6IjQ4YmZjZTIxLTc1ZTgtNDJkOS1hNDk5LTM2YzllMTEwNjliNyIsImVtYWlsIjoidGVzdGluZ0BzdGFycy1maXUuY29tIiwicGhvbmUiOiIiLCJhcHBfbWV0YWRhdGEiOnsicHJvdmlkZXIiOiJlbWFpbCIsInByb3ZpZGVycyI6WyJlbWFpbCJdfSwidXNlcl9tZXRhZGF0YSI6e30sInJvbGUiOiJhdXRoZW50aWNhdGVkIiwiYWFsIjoiYWFsMSIsImFtciI6W3sibWV0aG9kIjoicGFzc3dvcmQiLCJ0aW1lc3RhbXAiOjE3MDg1Njc0NDB9XSwic2Vzc2lvbl9pZCI6IjFkMmI2NGNlLWQwYjYtNDgyYi1hOTA5LWVhOGM4YjM2NmJmMyJ9.FHHroQDe5pI7GdBSp94KFhAAMPq4JujMnClD4D9mEpY",
    "token_type": "bearer",
    "expires_in": 3600,
    "expires_at": 1708750432,
    "refresh_token": "P8758SVusMv0rHaYUKUVgQ",
    "user": {
        "id": "48bfce21-75e8-42d9-a499-36c9e11069b7",
        "aud": "authenticated",
        "role": "authenticated",
        "email": "testing@stars-fiu.com",
        "email_confirmed_at": "2024-01-30T21:46:43.062044Z",
        "phone": "",
        "confirmed_at": "2024-01-30T21:46:43.062044Z",
        "last_sign_in_at": "2024-02-22T02:04:00.346767Z",
        "app_metadata": {
            "provider": "email",
            "providers": [
                "email"
            ]
        },
        "user_metadata": {},
        "identities": [
            {
                "identity_id": "1f187a5d-ab5d-43f5-a14b-924cddb65f0c",
                "id": "48bfce21-75e8-42d9-a499-36c9e11069b7",
                "user_id": "48bfce21-75e8-42d9-a499-36c9e11069b7",
                "identity_data": {
                    "email": "testing@stars-fiu.com",
                    "email_verified": false,
                    "phone_verified": false,
                    "sub": "48bfce21-75e8-42d9-a499-36c9e11069b7"
                },
                "provider": "email",
                "last_sign_in_at": "2024-01-30T21:46:43.059612Z",
                "created_at": "2024-01-30T21:46:43.059689Z",
                "updated_at": "2024-01-30T21:46:43.059689Z",
                "email": "testing@stars-fiu.com"
            }
        ],
        "created_at": "2024-01-30T21:46:43.047451Z",
        "updated_at": "2024-02-24T03:53:52.086786Z"
    }
}

4. Copy the access_token and paste it into the body of the request below:
  {token: "the string you copied"}
5. Send the request and you should get a response with the decoded token.
"""
