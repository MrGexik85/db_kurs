from pydantic import BaseModel, Field

from v1.supplies.schema import ShortProduct
from v1.bank_account.schema import BankAccount


class CreateContractor(BaseModel):
    title: str = Field(description='Название поставщика', example='ООО ЛенСтрой')
    address: str = Field(description='Адрес поставщика', example='Пушкина, 22')
    director: str = Field(description='Директор', example='Иванов И.А.')
    accountant: str = Field(description='Бухгалтер', example='Сидорова А.И.')
    bank_account_id: int = Field(description='Идентификатор банковского счета', example=2)


class Contractor(BaseModel):
    id: int = Field(description='Идентификатор поставщика', example=1)
    title: str = Field(description='Название поставщика', example='ООО ЛенСтрой')
    address: str = Field(description='Адрес поставщика', example='Пушкина, 22')
    director: str = Field(description='Директор', example='Иванов И.А.')
    accountant: str = Field(description='Бухгалтер', example='Сидорова А.И.')
    bank_account: BankAccount = Field()
    products: list[ShortProduct] = Field()