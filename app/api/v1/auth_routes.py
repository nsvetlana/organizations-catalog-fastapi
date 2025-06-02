from datetime import timedelta
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.auth import create_access_token
from app.config import settings

router = APIRouter()

class TokenRequest(BaseModel):
    client_id: str
    client_secret: str  # This is your API key used for token exchange

@router.post("/token")
def token_exchange(token_request: TokenRequest):
    """
    Perform an OAuth2 token exchange.
    The client sends a JSON object with:
      - client_id: an identifier for the client
      - client_secret: the API key; if valid, a JWT token is issued.
    """
    if token_request.client_secret != settings.API_KEY:
         raise HTTPException(
              status_code=status.HTTP_401_UNAUTHORIZED,
              detail="Invalid API_KEY provided for token exchange"
         )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
         data={"sub": token_request.client_id},
         expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
