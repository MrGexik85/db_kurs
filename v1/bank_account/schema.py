from pydantic import BaseModel, Field

class CreateBankAccountRequest(BaseModel):
    bank_name: str = Field(description='Название банка', example='Сбербанк')
    inn: str = Field(description='ИНН', example='23112344')
    bik: str = Field(description='БИК', example='31256942')
    account: str = Field(description='Номер счета', example='4128594125484712395')


class BankAccount(BaseModel):
    id: int = Field(description='Уникальный идентификатор', example=2)
    bank_name: str = Field(description='Название банка', example='Сбербанк')
    inn: str = Field(description='ИНН', example='23112344')
    bik: str = Field(description='БИК', example='31256942')
    account: str = Field(description='Номер счета', example='4128594125484712395')


class UpdateBankAccount(BaseModel):
    bank_name: str | None = Field(default=None, description='Название банка', example='Сбербанк')
    inn: str | None = Field(default=None, description='ИНН', example='23112344')
    bik: str | None = Field(default=None, description='БИК', example='31256942')
    account: str | None = Field(default=None, description='Номер счета', example='4128594125484712395')
