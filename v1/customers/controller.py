from fastapi import HTTPException, status
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from sqlalchemy.sql import text

from v1.auth.schema import ResponseSuccess

from .schema import Customer, BankAccount


async def set_customer_bank_account_controller(db: Session, customerId: int, bankId: int):
    sql_query = f"""UPDATE customers
	    SET bank_account_id= {bankId}
	    WHERE id={customerId};"""

    try:
        db.execute(sql_query)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Something wrong')
    
    return ResponseSuccess()


async def get_customers_controller(db: Session):
    sql_query = f"""SELECT cr.*, bk.*
	    FROM customers AS cr
	    JOIN bank_accounts AS bk ON bk.id = cr.bank_account_id;"""
    
    
    customers = db.execute(sql_query).all()


    return list(map(
        lambda customer: Customer(
            id=customer[0],
            title=customer[1],
            address=customer[2],
            phone=customer[3],
            first_name=customer[4],
            middle_name=customer[5],
            last_name=customer[6],
            bank_account=BankAccount(
                id=customer[7],
                bank_name=customer[11],
                inn=customer[12],
                bik=customer[13],
                account=customer[14]
            ),
            notes=customer[8]
        ),
        customers
    ))


async def get_customer_by_id_controller(db: Session, customerId: int):
    sql_query = f"""SELECT cr.*, bk.*
	    FROM customers AS cr
	    JOIN bank_accounts AS bk ON bk.id = cr.bank_account_id
        WHERE cr.id = {customerId};"""
    
    try:
        customer = db.execute(sql_query).one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Customer not found')
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Something wrong')


    return Customer(
        id=customer[0],
        title=customer[1],
        address=customer[2],
        phone=customer[3],
        first_name=customer[4],
        middle_name=customer[5],
        last_name=customer[6],
        bank_account=BankAccount(
            id=customer[7],
            bank_name=customer[11],
            inn=customer[12],
            bik=customer[13],
            account=customer[14]
        ),
        notes=customer[8]
    )