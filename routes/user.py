
from fastapi import APIRouter, Response, Depends, status, HTTPException
from config.db import conn
from models.user import UsersModel
from schemas.user import UserSchemas
import bcrypt
from auth import AuthHandler


UserRouter = APIRouter()

auth_handler = AuthHandler()

@UserRouter.get("/users")
def get_users(v=Depends(auth_handler.auth_wrapper)):
  return conn.execute(UsersModel.select()).fetchall()


@UserRouter.post("/users", response_model=UserSchemas)
def create_user(user: UserSchemas, v=Depends(auth_handler.auth_wrapper)):

  userEmail = conn.execute(UsersModel.select().where(UsersModel.c.email == user.email)).first()

  if (userEmail is not None):
    raise HTTPException(
      status_code=status.HTTP_412_PRECONDITION_FAILED, 
      detail='Email ya registrado'
    )

  hashed_password = auth_handler.get_password_hash(user.password)

  new_user = {
    "firstName": user.firstName, 
    "lastName": user.lastName, 
    "rol": user.rol, 
    "status": user.status, 
    "email": user.email, 
    "password": hashed_password
  }

  result = conn.execute(UsersModel.insert().values(new_user))
  return conn.execute(UsersModel.select().where(UsersModel.c.id == result.lastrowid)).first()


@UserRouter.get("/user/{id}")
def get_user(id: int, v=Depends(auth_handler.auth_wrapper)):
  return conn.execute(UsersModel.select().where(UsersModel.c.id == id)).first()


@UserRouter.delete("/user/{id}")
def delete_user(id: int, v=Depends(auth_handler.auth_wrapper)):
  conn.execute(UsersModel.delete().where(UsersModel.c.id == id))
  return Response(status_code=status.HTTP_204_NO_CONTENT)