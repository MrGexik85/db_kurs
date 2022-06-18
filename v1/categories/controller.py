from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from v1.auth.schema import ResponseSuccess
from .schema import CategoryResponse, CreateCategoryRequest


async def get_categories_controller(db: Session):
    sql_query = text("""SELECT id, name FROM categories;""")

    rows = db.execute(sql_query).all()

    return list(map(
        lambda x: CategoryResponse(id=x[0], name=x[1]),
        rows
    ))


async def create_category_controller(db: Session, body: CreateCategoryRequest):
    sql_query = text(f"""INSERT INTO categories(name) VALUES ('{body.name}');""")

    try:
        db.execute(sql_query)
        db.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Something wrong')
    
    return ResponseSuccess()


async def get_category_by_id_controller(db: Session, id: int):
    sql_query = text(f"""SELECT id, name FROM categories WHERE id = {id};""")

    try:
        row = db.execute(sql_query).one()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')
    
    return CategoryResponse(id=row[0], name=row[1])


async def update_category_by_id_controller(db: Session, id: int, body: CreateCategoryRequest):
    sql_query = text(f"""UPDATE categories SET name='{body.name}' WHERE id = {id};""")

    try:
        db.execute(sql_query)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Something wrong')
    
    return ResponseSuccess()


async def delete_category_by_id_controller(db: Session, id: int):
    sql_query = text(f"""DELETE FROM categories WHERE id = {id};""")

    try:
        db.execute(sql_query)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Something wrong')
    
    return ResponseSuccess()