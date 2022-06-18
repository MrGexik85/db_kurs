from pydantic import BaseModel, Field

class CreateBankAccountRequest(BaseModel):
    bank_name: str = Field(description='Название банка', example='Сбербанк')
    inn: str = Field(description='ИНН', example='23112344')
    bik: str = Field(description='БИК', example='31256942')
    account: str = Field(description='Номер счета', example='Сбербанк')