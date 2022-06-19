from fastapi import HTTPException, status
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from v1.auth.schema import ResponseSuccess

from .schema import SupplyResponse, ShortContractor, ShortProduct, CreateSupply



async def get_supplies_controller(db: Session, date_from: date | None, date_to: date | None):
    if (date_from is not None) and (date_to is not None):
        sql_query = text(f"""SELECT ps.*, ct.title, pr.title
	                            FROM product_supplies AS ps
	                            JOIN contractors AS ct ON ct.id = ps.contractor_id
	                            JOIN products AS pr ON pr.id = ps.product_id
	                            WHERE ps.date >= '{date_from}' AND ps.date <= '{date_to} 23:59:59';""")
    else: 
        sql_query = text(f"""SELECT ps.*, ct.title, pr.title
	                            FROM product_supplies AS ps
	                            JOIN contractors AS ct ON ct.id = ps.contractor_id
	                            JOIN products AS pr ON pr.id = ps.product_id;""")
    
    rows = db.execute(sql_query).all()

    return list(map(
        lambda x: SupplyResponse(
            id=x[0],
            contractor=ShortContractor(id=x[1], title=x[5]),
            product=ShortProduct(id=x[2], title=x[6]),
            amount=x[3],
            date=x[4]
        ),
        rows
    ))


async def get_supplies_by_product_id_controller(db: Session, productId: int, date_from: date | None, date_to: date | None):
    if (date_from is not None) and (date_to is not None):
        sql_query = text(f"""SELECT ps.*, ct.title, pr.title
	                            FROM product_supplies AS ps
	                            JOIN contractors AS ct ON ct.id = ps.contractor_id
	                            JOIN products AS pr ON pr.id = ps.product_id
	                            WHERE ps.date >= '{date_from}' AND ps.date <= '{date_to} 23:59:59' AND ps.product_id = {productId};""")
    else: 
        sql_query = text(f"""SELECT ps.*, ct.title, pr.title
	                            FROM product_supplies AS ps
	                            JOIN contractors AS ct ON ct.id = ps.contractor_id
	                            JOIN products AS pr ON pr.id = ps.product_id
                                WHERE ps.product_id = {productId};""")
    
    rows = db.execute(sql_query).all()

    return list(map(
        lambda x: SupplyResponse(
            id=x[0],
            contractor=ShortContractor(id=x[1], title=x[5]),
            product=ShortProduct(id=x[2], title=x[6]),
            amount=x[3],
            date=x[4]
        ),
        rows
    ))


async def create_supply_controller(db: Session, body: CreateSupply):
    sql_query = text(f"""INSERT INTO product_supplies(
	        contractor_id, product_id, amount, date)
	        VALUES ({body.contractor_id}, {body.product_id}, {body.amount}, '{body.date}');""")

    try:
        db.execute(sql_query)
        db.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product id or contract id not found')

    return ResponseSuccess()