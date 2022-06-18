from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from sqlalchemy.sql import text
from .schema import CreateBankAccountRequest, BankAccount, UpdateBankAccount

from v1.auth.schema import ResponseSuccess


async def create_bank_account_controller(db: Session, body: CreateBankAccountRequest):
    sql_query = text(f"""INSERT INTO bank_accounts(
	bank_name, inn, bik, account)
	VALUES ('{body.bank_name}', '{body.inn}', '{body.bik}', '{body.account}');""")

    try:
        db.execute(sql_query)
        db.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Something wrong')
    
    return ResponseSuccess()


async def get_bank_account_by_id_controller(db: Session, id: int):
    sql_query = text(f"""SELECT * from bank_accounts WHERE id = {id}""")

    try:
        row = db.execute(sql_query).one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Bank account not found')
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Something wrong')
    
    return BankAccount(
        id=row[0],
        bank_name=row[1],
        inn=row[2],
        bik=row[3],
        account=row[4]
    )


async def update_bank_account_by_id_controller(db: Session, id: int, body: UpdateBankAccount):
    expression = ""
    expression += f"bank_name='{body.bank_name}', " if body.bank_name else ""
    expression += f"inn='{body.inn}', " if body.inn else ""
    expression += f"bik='{body.bik}', " if body.bik else ""
    expression += f"account={body.account}, " if body.account else ""
    expression = expression[:-2]

    sql_query = text(f"""UPDATE bank_accounts
	SET {expression}
	WHERE id = {id};""")

    try:
        db.execute(sql_query)
        db.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Something wrong')
    
    return ResponseSuccess()
