from typing import Optional
from pydantic import  BaseModel

class UserSchemas(BaseModel):
  id: Optional[int]
  firstName: str
  lastName: str
  rol: str
  status: str
  email: str
  password: str
