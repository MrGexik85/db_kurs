from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy.exc import NoResultFound

from v1.auth.schema import ResponseSuccess
from v1.user.schema import UserSession
from v1.product.schema import CreateProduct, ProductResponse, Category, ProductUpdateRequest




async def create_new_product_controller(db: Session, user: UserSession, body: CreateProduct) -> CreateProduct:
    if body.description:
        fields = 'title, description, image_url, price, "package", category_id'
        values = f"'{body.title}', '{body.description}', '{body.image_url}', {body.price}, '{body.package}', {body.category_id}"
    else:
        fields = 'title, image_url, price, "package", category_id'
        values = f"'{body.title}', '{body.image_url}', {body.price}, '{body.package}', {body.category_id}"

    try:
        expression = text(f"""INSERT INTO products({fields}) VALUES ({values});""")
        db.execute(expression)
        db.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Something wrong')
    
    return body


async def get_products_controller(db: Session, category_id: int | None) -> list[ProductResponse]:
    expr = f'WHERE pr.category_id = {category_id}' if (category_id is not None) else ''
    sql_query = text(f"""SELECT pr.*, ca.name, oi.sold, ps.supplied FROM products AS pr
	                    JOIN categories AS ca ON ca.id = pr.category_id
	                    LEFT JOIN (SELECT oi_tmp.product_id, SUM(oi_tmp.product_count) AS sold FROM order_items AS oi_tmp GROUP BY oi_tmp.product_id) AS oi ON oi.product_id = pr.id
	                    LEFT JOIN (SELECT ps_temp.product_id, SUM(ps_temp.amount) AS supplied FROM product_supplies AS ps_temp GROUP BY ps_temp.product_id) AS ps ON ps.product_id = pr.id
 	                    {expr};""")

    answ = db.execute(sql_query).all()
    return list(map(
        _process_product_db_answer_tuple,
        answ
    ))


def _process_product_db_answer_tuple(x):
    sold = x[8] if x[8] else 0
    supply = x[9] if x[9] else 0
    return ProductResponse(
            id=x[0], 
            title=x[1], 
            description=x[2],
            image_url=x[3],
            price=x[4],
            package=x[5],
            category=Category(id=x[6], name=x[7]),
            remaind=supply-sold
    )


async def get_product_by_id_controller(db: Session, id: int) -> ProductResponse:
    expr = f'WHERE pr.id = {id}'
    sql_query = text(f"""SELECT pr.*, ca.name, oi.sold, ps.supplied FROM products AS pr
	                    JOIN categories AS ca ON ca.id = pr.category_id
	                    LEFT JOIN (SELECT oi_tmp.product_id, SUM(oi_tmp.product_count) AS sold FROM order_items AS oi_tmp GROUP BY oi_tmp.product_id) AS oi ON oi.product_id = pr.id
	                    LEFT JOIN (SELECT ps_temp.product_id, SUM(ps_temp.amount) AS supplied FROM product_supplies AS ps_temp GROUP BY ps_temp.product_id) AS ps ON ps.product_id = pr.id
 	                    {expr};""")

    try:
        answ = db.execute(sql_query).one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Something wrong')
    
    sold = answ[8] if answ[8] else 0
    supply = answ[9] if answ[9] else 0
    return ProductResponse(
            id=answ[0], 
            title=answ[1], 
            description=answ[2],
            image_url=answ[3],
            price=answ[4],
            package=answ[5],
            category=Category(id=answ[6], name=answ[7]),
            remaind=supply-sold
    )


async def delete_product_by_id_controller(db: Session, id: int) -> ResponseSuccess:
    sql_query = text(f"""DELETE FROM products AS pr WHERE pr.id = {id};""")
    print(sql_query)
    try:
        db.execute(sql_query)
        db.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Something wrong')
    
    return ResponseSuccess()


async def update_product_by_id_controller(db: Session, id: int, body: ProductUpdateRequest) -> ResponseSuccess:
    expression = ""
    expression += f"title='{body.title}', " if body.title else ""
    expression += f"description='{body.description}', " if body.description else ""
    expression += f"image_url='{body.image_url}', " if body.image_url else ""
    expression += f"price={body.price}, " if body.price else ""
    expression += f""""package"='{body.package}', """ if body.package else ""
    expression = expression[:-2]

    sql_query = text(f"""UPDATE products
	        SET {expression}
	        WHERE id = {id};""")
    
    print(sql_query)
    try:
        db.execute(sql_query)
        db.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Something wrong')

    return ResponseSuccess()

