from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from v1.auth.schema import ResponseSuccess

from .schema import CreateContractor, Contractor, BankAccount, ShortProduct


async def create_contractor_controller(db: Session, body: CreateContractor):
    sql_query = f"""INSERT INTO public.contractors(
	title, address, director, accountant, bank_account_id)
	VALUES ('{body.title}', '{body.address}', '{body.director}', '{body.accountant}', {body.bank_account_id});"""

    try:
        db.execute(sql_query)
        db.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Cant create new contractor')

    return ResponseSuccess()


async def get_contractors_controller(db: Session):
    sql_query = """SELECT cr.*, bk.*
	    FROM contractors AS cr
	    JOIN bank_accounts AS bk ON bk.id = cr.bank_account_id;"""
    
    rows = db.execute(sql_query).all()

    def _prepare_contractor(contractor):
        nonlocal db
        query = f"""SELECT pr.id, pr.title
	        FROM product_contractor_association AS pca
	        JOIN products as pr ON pca.product_id = pr.id
            WHERE pca.contractor_id = {contractor[0]};"""
        
        products = db.execute(query).all()

        return Contractor(
            id=contractor[0],
            title=contractor[1],
            address=contractor[2],
            director=contractor[3],
            accountant=contractor[4],
            bank_account=BankAccount(
                id=contractor[6],
                bank_name=contractor[7],
                inn=contractor[8],
                bik=contractor[9],
                account=contractor[10]
            ),
            products=list(map(
                lambda x: ShortProduct(id=x[0], title=x[1]),
                products
            ))
        )

    return list(map(
        _prepare_contractor,
        rows
    ))



async def get_contractor_by_id_controller(db: Session, id: int):
    sql_query = f"""SELECT cr.*, bk.*
	    FROM contractors AS cr
	    JOIN bank_accounts AS bk ON bk.id = cr.bank_account_id
        WHERE cr.id = {id};"""
    
    try:
        contractor = db.execute(sql_query).one()
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contractor not found')


    query = f"""SELECT pr.id, pr.title
        FROM product_contractor_association AS pca
        JOIN products as pr ON pca.product_id = pr.id
        WHERE pca.contractor_id = {contractor[0]};"""
    
    products = db.execute(query).all()

    return Contractor(
        id=contractor[0],
        title=contractor[1],
        address=contractor[2],
        director=contractor[3],
        accountant=contractor[4],
        bank_account=BankAccount(
            id=contractor[6],
            bank_name=contractor[7],
            inn=contractor[8],
            bik=contractor[9],
            account=contractor[10]
        ),
        products=list(map(
            lambda x: ShortProduct(id=x[0], title=x[1]),
            products
        ))
    )


async def create_contractor_product_association_controller(db: Session, contractorId: int, productId: int):
    sql_query = f"""INSERT INTO product_contractor_association(
	    product_id, contractor_id)
	    VALUES ({productId}, {contractorId});"""
    
    try:
        db.execute(sql_query)
        db.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Something wrong')
    
    return ResponseSuccess()


async def delete_contractor_product_association_controller(db: Session, contractorId: int, productId: int):
    sql_query = f"""DELETE FROM product_contractor_association
	    WHERE product_id = {productId} AND contractor_id = {contractorId};"""

    db.execute(sql_query)
    db.commit()
    
    return ResponseSuccess()


async def set_contractor_bank_account_controller(db: Session, contractorId: int, bankId: int):
    sql_query = f"""UPDATE contractors
	SET bank_account_id={bankId}
	WHERE id = {contractorId};"""

    try:
        db.execute(sql_query)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Something wrong')
    
    return ResponseSuccess()