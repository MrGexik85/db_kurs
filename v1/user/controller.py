from fastapi import HTTPException, status
from datetime import date, datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from sqlalchemy.sql import text
from random import randint

from v1.auth.schema import ResponseSuccess
from v1.orders.schema import Order, Product, Customer, Category
from .schema import UserSession, CreateUserOrder



async def create_user_order_controller(db: Session, user: UserSession, body: CreateUserOrder):
    sql_query = text(f"""SELECT pr.*, oi.sold, ps.supplied FROM products AS pr
	                    LEFT JOIN (SELECT oi_tmp.product_id, SUM(oi_tmp.product_count) AS sold FROM order_items AS oi_tmp GROUP BY oi_tmp.product_id) AS oi ON oi.product_id = pr.id
	                    LEFT JOIN (SELECT ps_temp.product_id, SUM(ps_temp.amount) AS supplied FROM product_supplies AS ps_temp GROUP BY ps_temp.product_id) AS ps ON ps.product_id = pr.id
 	                    WHERE pr.id = {body.productId};""")

    try:
        answ = db.execute(sql_query).one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Something wrong')

    remaind = answ[8] - answ[7]

    sql_query = f"""SELECT id from customers WHERE user_id = {user.id}"""
    try:
        answ = db.execute(sql_query).one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='You are not a customer')
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Something wrong')

    if body.amount > remaind:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Not enought product in storage')

    sql_query = f"""
    BEGIN TRANSACTION;

    WITH last_id AS (
        INSERT INTO orders(
        "number", date, note, delivery_terms, customer_id, is_paid, is_deliver)
        VALUES ({randint(10000000, 99999999)}, '{str(datetime.now())}', '{body.notes}', '{body.delivery_terms}', {answ[0]}, false, false)
        RETURNING id
    )

    INSERT INTO order_items(
        order_id, product_id, product_count)
        VALUES ((SELECT id from last_id LIMIT 1), {body.productId}, {body.amount});

    COMMIT TRANSACTION;
    """

    try:
        db.execute(sql_query)
        db.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Something wrong')
    
    return ResponseSuccess()


async def get_user_orders_controller(db: Session, user: UserSession):
    sql_query = f"""SELECT id from customers WHERE user_id = {user.id}"""
    try:
        answ = db.execute(sql_query).one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='You are not a customer')
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Something wrong')

    sql_query = f"""SELECT od.*, cs.title, cs.address, cs.phone, cs.first_name, cs.last_name
	    FROM orders AS od
	    JOIN customers AS cs ON cs.id = od.customer_id
        WHERE od.customer_id = {answ[0]}"""
    
    rows = db.execute(sql_query).all()
    
    def _prepare_order_rows(order):
        nonlocal db
        sql_query = f"""SELECT oi.*, pr.*
        FROM order_items AS oi
        JOIN (
            SELECT pr1.*, ca.name 
            FROM products AS pr1 
            JOIN categories AS ca ON ca.id = pr1.category_id)
        AS pr ON pr.id = oi.product_id
        WHERE order_id = {order[0]};"""

        products = db.execute(sql_query).all()

        return Order(
            id=order[0],
            number=order[1],
            date=order[2],
            note=order[3],
            delivery_terms=order[4],
            is_paid=order[6],
            is_deliver=order[7],
            customer=Customer(
                id=order[5],
                title=order[8],
                address=order[9],
                phone=order[10],
                first_name=order[11],
                last_name=order[12]
            ),
            products=list(map(
                lambda x: Product(
                    id=x[2],
                    title=x[5],
                    description=x[6],
                    image_url=x[7],
                    price=x[8],
                    count=x[3],
                    package=x[9],
                    category=Category(
                        id=x[10],
                        name=x[11]
                    )
                ),
                products
            ))
        )

    return list(map(
        _prepare_order_rows,
        rows
    ))


async def delete_user_order_controller(db: Session, user: UserSession, orderId: int):
    sql_query = f"""SELECT id from customers WHERE user_id = {user.id}"""
    try:
        answ = db.execute(sql_query).one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='You are not a customer')
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Something wrong')

    print(answ[0])
    sql_query = f"""DELETE FROM orders
	    WHERE id = {orderId} AND customer_id = {answ[0]};"""
    
    try:    
        db.execute(sql_query)
        db.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Something wrong')
    
    return ResponseSuccess()


async def get_user_order_by_id_controller(db: Session, user: UserSession, orderId: int):
    sql_query = f"""SELECT id from customers WHERE user_id = {user.id}"""
    try:
        answ = db.execute(sql_query).one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='You are not a customer')
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Something wrong')

    sql_query = f"""SELECT od.*, cs.title, cs.address, cs.phone, cs.first_name, cs.last_name
	    FROM orders AS od
	    JOIN customers AS cs ON cs.id = od.customer_id
        WHERE od.customer_id = {answ[0]} AND od.id = {orderId}"""
    
    try:
        order = db.execute(sql_query).one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Order not found')
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Something wrong')
    

    sql_query = f"""SELECT oi.*, pr.*
    FROM order_items AS oi
    JOIN (
        SELECT pr1.*, ca.name 
        FROM products AS pr1 
        JOIN categories AS ca ON ca.id = pr1.category_id)
    AS pr ON pr.id = oi.product_id
    WHERE order_id = {order[0]};"""

    products = db.execute(sql_query).all()

    return Order(
        id=order[0],
        number=order[1],
        date=order[2],
        note=order[3],
        delivery_terms=order[4],
        is_paid=order[6],
        is_deliver=order[7],
        customer=Customer(
            id=order[5],
            title=order[8],
            address=order[9],
            phone=order[10],
            first_name=order[11],
            last_name=order[12]
        ),
        products=list(map(
            lambda x: Product(
                id=x[2],
                title=x[5],
                description=x[6],
                image_url=x[7],
                price=x[8],
                count=x[3],
                package=x[9],
                category=Category(
                    id=x[10],
                    name=x[11]
                )
            ),
            products
        ))
    )