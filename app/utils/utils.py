from argon2 import PasswordHasher
from app.settings.config import SECRET_KEY, ALGORITHM, TOKEN_EXPIRATION_TIME_MINUTES

ph = PasswordHasher()

import jwt
from datetime import timedelta, datetime


def generate_token(email):
    # now + token lifespan
    expiration_time = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_TIME_MINUTES)
    payload = {
        "sub": email,
        "exp": expiration_time,
        
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    return token
