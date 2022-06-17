from pydantic import BaseModel, Field, EmailStr


class RequestRegisterSchema(BaseModel):
    username: str = Field(description='Логин пользователя', example="superman227")
    password: str = Field(description='Самый сложный пароль в мире', example='qwertyu')


class RequestLoginSchema(BaseModel):
    username: str = Field(description='Никнейм пользователя', example="ivan228")
    password: str = Field(description='Самый сложный пароль в мире', example='qwertyu')


class ResponseSuccess(BaseModel):
    detail: str = Field(default='Success')


class ResponseLoginSuccess(BaseModel):
    id: int = Field(default=2)
    username: str = Field(default="superman")
    isAdmin: bool = Field(default=False)


login_invalid_responses = responses_authenticate = {
    401: {
        "description": "Authentication Failed",
        "content": { 
            "application/json": {
                "examples": { 
                    "wrong_username_or_password": {
                        "summary": "Wrong username or/and password",
                        "value": { "detail": "Wrong username or/and password" }
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
                    "Username already exist": {
                        "summary": "Username already exist",
                        "value": { "detail": "Username already exist" }
                    }
                }
            } 
        }
    }
}