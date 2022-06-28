from fastapi import FastAPI, HTTPException, status, Depends, Form
from routes.user import UserRouter
from models.user import UsersModel
from schemas.user import UserSchemas
from config.db import conn
from auth import AuthHandler
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(UserRouter)

auth_handler = AuthHandler()

@app.post("/login")
def login(email: str = Form(), password: str = Form()):

  dataUser = conn.execute(UsersModel.select().where(UsersModel.c.email == email)).first()

  if (dataUser is None):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED, 
      detail='Email o contraseña invalida'
    )
  
  has_password = dataUser['password']

  if (not auth_handler.verify_password(password, has_password)):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED, 
      detail='Email o contraseña invalida'
    )

  if (dataUser['status'] != 'active'):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED, 
      detail='Usuario inactivo'
    )

  name = "{} {}".format(dataUser['firstName'], dataUser['lastName'])

  token = auth_handler.encode_token(email, name, dataUser['rol'] )
  return { 'token': token }


@app.get("/validateToken")
def validateToken(token: str):
  v = auth_handler.decode_token(token)

  if(v):
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED)


@app.get('/protected')
def protected(data1: str, data2: str, v=Depends(auth_handler.auth_wrapper)):
    return { 'email': v, 'data1': data1, 'data2': data2 }
