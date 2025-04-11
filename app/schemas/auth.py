from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class WebAuthnRegistrationStart(BaseModel):
    email: str

class WebAuthnRegistrationFinish(BaseModel):
    credential: dict
    
