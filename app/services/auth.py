import jwt
from fastapi import HTTPException 
from datetime import datetime, timedelta
from ..config import settings
from app.models import schemas

class Auth():

    secret = settings.secret
    def encode_token(self, id:str):
        payload = {
            'exp' : datetime.utcnow() + timedelta(days=0, minutes=50),
            'iat' : datetime.utcnow(),
        'scope': 'token',
            'sub' : id
        }
        return jwt.encode(
            payload, 
            self.secret,
            algorithm='HS256'
        )

    def decode_token(self, token:str):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            if (payload['scope'] == 'token'):
                return payload['sub'] 
               
                   
            raise HTTPException(status_code=401, detail='Scope for the token is invalid')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Token expired')
    