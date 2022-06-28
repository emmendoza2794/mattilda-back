from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta, engine

UsersModel = Table("users", meta, 
  Column("id", Integer, primary_key=True),
  Column("firstName", String(50)),
  Column("lastName", String(50)),
  Column("rol", String(50)),
  Column("status", String(50)),
  Column("email", String(50), unique=True),
  Column("password", String(255))
)

meta.create_all(engine)