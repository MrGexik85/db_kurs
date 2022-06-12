from pydantic import BaseModel, Field, EmailStr


class RequestRegisterSchema(BaseModel):
    username: str = Field(description='Логин пользователя', example="superman227")
    password: str = Field(description='Самый сложный пароль в мире', example='qwertyu')


class RequestLoginSchema(BaseModel):
    username: EmailStr = Field(description='Никнейм пользователя', example="ivan228")
    password: str = Field(description='Самый сложный пароль в мире', example='qwertyu')


class ResponseSuccess(BaseModel):
    detail: str = Field(default='Success')


class ResponseLoginSuccess(BaseModel):
    username: str = Field(default="superman")
    isAdmin: bool = Field(default=False)


login_invalid_responses = responses_authenticate = {
    401: {
        "description": "Authentication Failed",
        "content": { 
            "application/json": {
                "examples": { 
                    "wrong_email_or_password": {
                        "summary": "Wrong email or/and password",
                        "value": { "detail": "Wrong email or/and password" }
                    }
                }
            } 
        }
    }
}

register_invalid_responses = responses_authenticate = {
    401: {
        "description": "Authentication Failed",
        "content": { 
            "application/json": {
                "examples": { 
                    "Username or email already exist": {
                        "summary": "Username or email already exist",
                        "value": { "detail": "Username or email already exist" }
                    }
                }
            } 
        }
    }
}