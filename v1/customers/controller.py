from fastapi import HTTPException, status
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from v1.auth.schema import ResponseSuccess


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