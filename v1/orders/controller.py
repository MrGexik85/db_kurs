from fastapi import HTTPException, status
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from v1.auth.schema import ResponseSuccess

from .schema import Order, Product, Customer, Category


async def get_orders_controller(db: Session, is_paid: bool | None, is_deliver: bool | None, period_from: date | None, period_to: date | None):
    sql_query = """SELECT od.*, cs.title, cs.address, cs.phone, cs.first_name, cs.last_name
	    FROM orders AS od
	    JOIN customers AS cs ON cs.id = od.customer_id"""

    if (period_from is not None) and (period_to is not None):
        if is_paid is not None:
            if is_deliver is not None:
                sql_query += f""" WHERE date >= '{period_from}' AND date <= '{period_to} 23:59:59' AND is_paid = {is_paid} AND is_deliver = {is_deliver};"""
            else:
                sql_query += f""" WHERE date >= '{period_from}' AND date <= '{period_to} 23:59:59' AND is_paid = {is_paid};"""
        else:
            if is_deliver is not None:
                sql_query += f""" WHERE date >= '{period_from}' AND date <= '{period_to} 23:59:59' AND is_deliver = {is_deliver};"""
            else:
                sql_query += f""" WHERE date >= '{period_from}' AND date <= '{period_to} 23:59:59';"""
    else:
        if is_paid is not None:
            if is_deliver is not None:
                sql_query += f""" WHERE is_paid = {is_paid} AND is_deliver = {is_deliver};"""
            else:
                sql_query += f""" WHERE is_paid = {is_paid};"""
        else:
            if is_deliver is not None:
                sql_query += f""" WHERE is_deliver = {is_deliver};"""
            else:
                sql_query += f""";"""
    
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


async def set_paid_order_controller(db: Session, id: int):
    sql_query = text(f"""SELECT * FROM orders WHERE id = {id}""")

    try:
        db.execute(sql_query).one()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Order not found')
    
    sql_query = text(f"""UPDATE orders
	        SET is_paid=true
	WHERE id = {id};""")

    try:
        db.execute(sql_query)
        db.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Something wrong')
    
    return ResponseSuccess()




async def set_deliver_order_controller(db: Session, id: int):
    sql_query = text(f"""SELECT * FROM orders WHERE id = {id}""")

    try:
        db.execute(sql_query).one()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Order not found')
    
    sql_query = text(f"""UPDATE orders
	        SET is_deliver=true
	WHERE id = {id};""")

    try:
        db.execute(sql_query)
        db.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Something wrong')
    
    return ResponseSuccess()