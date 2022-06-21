from pydantic import BaseModel, Field
from v1.contractors.schema import BankAccount


class Customer(BaseModel):
    id: int = Field(description='Идентификатор клиента', example=2)
    title: str = Field(description='Наименование', example='Магазин')
    address: str = Field(description='Адрес', example='Коробкова, 22')
    phone: str = Field(description='Телефон', example='8953412342')
    first_name: str = Field(description='Имя', example='Леха')
    middle_name: str | None = Field(description='Отчество', example='Евгеньевич')
    last_name: str = Field(description='Фамилия', example='Русланов')
    bank_account: BankAccount = Field()
    notes: str = Field(description='Заметки к заказу', example='Доставить до 5 июля')