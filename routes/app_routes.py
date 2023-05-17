from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException
from db.fake_db import db

home = APIRouter()

oauth2 = OAuth2PasswordBearer("/token")


@home.get("/")
def index():
    return "Hello world"


# Con Depends mandamos a llamar funciones exclusivas a esta ruta.
@home.get("/users/me")
def user(token: str = Depends(oauth2)):
    user = db.get(token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Permiso denegado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return "Ingreso exitoso."


@home.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.get(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Usuario o contraseña equivocados.")
    if not form_data.password == user["password"]:
        raise HTTPException(status_code=400, detail="Usuario o contraseña equivocados.")
    return {"access_token": form_data.username, "token_type": "bearer"}
