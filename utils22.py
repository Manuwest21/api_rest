from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta 

router1 = APIRouter()
security = OAuth2PasswordBearer(tokenUrl="token")  # Ajoutez ceci pour définir le schéma de sécurité OAuth2

ACCESS_TOKEN_EXPIRE_MINUTES = 30
# Informations d'identification "en dur" (nom d'utilisateur et mot de passe)
USER_CREDENTIALS = {
    "admin": "password123"
}

# Fonction pour vérifier les mots de passe hachés
def verify_password(plain_password, hashed_password):
    # Vous devrez remplacer cette fonction par votre propre logique de vérification de mot de passe
    # Par exemple, en utilisant la méthode de hachage que vous avez choisie (bcrypt, sha256, etc.)
    return plain_password == hashed_password

# Fonction pour vérifier l'accès avec JWT
async def has_access(credentials: HTTPAuthorizationCredentials = Depends(security)):
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

# Endpoint pour obtenir un jeton JWT
@router1.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    if username in USER_CREDENTIALS and verify_password(password, USER_CREDENTIALS[username]):
        # Si les informations d'identification sont correctes, générez un jeton JWT et retournez-le
        load_dotenv()
        SECRET_KEY = os.environ.get("SECRET_KEY")
        ALGORITHM = "HS256"
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {"sub": username, "exp": datetime.utcnow() + access_token_expires}
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": encoded_jwt, "token_type": "bearer"}
    else:
        # Sinon, lève une HTTPException avec un code d'état 401 (non autorisé)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
