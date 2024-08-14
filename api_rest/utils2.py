from fastapi import APIRouter, HTTPException, status, Depends
from jose import JWTError, jwt
import os
from pydantic import BaseModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv

router1 = APIRouter()  # Créez un routeur API

async def has_access(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    token = credentials.credentials
    load_dotenv()
    SECRET_KEY = os.environ.get("SECRET_KEY")
    ALGORITHM = "HS256"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
    except JWTError:
        raise credentials_exception
    if username == "admin":
        return True
    else:
        raise credentials_exception


# def generate_token(to_encode):
#     load_dotenv()
#     SECRET_KEY = os.environ.get("SECRET_KEY")
#     ALGORITHM = "HS256"
#     to_encode_dict = {"sub": to_encode}
#     encoded_jwt = jwt.encode(to_encode_dict, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# Exportez le routeur
