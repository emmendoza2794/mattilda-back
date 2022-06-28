import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
import hashlib


class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = 'M@tt!LdaSecret'

    def get_password_hash(self, password):
        en=password.encode()
        hex_result = hashlib.md5(en)
        return hex_result.hexdigest()

    def verify_password(self, plain_password, hashed_password):
        en = self.get_password_hash(plain_password)
        return en == hashed_password

    # def get_password_hash(self, password):
    #     password = bytes(password, 'utf-8')
    #     return self.pwd_context.hash(password)

    # def verify_password(self, plain_password, hashed_password):
    #     plain_password = bytes(plain_password, 'utf-8')
    #     hashed_password = bytes(hashed_password, 'utf-8')
    #     return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, email, name, rol):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
            'email': email,
            'name': name,
            'rol': rol
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return True
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Signature has expired')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='Invalid token')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)