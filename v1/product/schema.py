from pydantic import BaseModel, Field
from fastapi import Query


class CreateProduct(BaseModel):
    title: str = Field(example='AirPods Max')
    description: str | None = Field(default=None, example='Полноразмерные беспроводные наушники')
    image_url: str = Field(example="https://blabla.com/jpg")
    price: int = Field(example=20000)
    package: str = Field(example='Картон')
    category_id: int = Field(example=1)


class Category(BaseModel):
    id: int = Field(example=1)
    name: str = Field(example='AirPods Max')


class ProductResponse(BaseModel):
    id: int = Field(example=1)
    title: str = Field(example='AirPods Max')
    description: str | None = Field(default=None, example='Полноразмерные беспроводные наушники')
    image_url: str = Field(example="https://blabla.com/jpg")
    price: int = Field(example=20000)
    package: str = Field(example='Картон')
    category: Category = Field()
    remaind: int = Field(example=20)


class ProductUpdateRequest(BaseModel):
    title: str | None = Field(default=None, description='Новое название', example='New AirPods Max') 
    description: str | None = Field(default=None, description='Новое описание', example='Обновили описание')
    image_url: str | None = Field(default=None, description='Новое фото', example='http://example.com/new_photo.jpg')
    price: int | None = Field(default=None, description='Новая цена', example=21000) 
    package: str | None = Field(default=None, description='Новая упаковка', example='Пластик')
