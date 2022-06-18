from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from .schema import ProductStorage


async def get_storage_products_controller(db: Session):
    sql_query = text(f"""SELECT pr.id, pr.title, oi.sold, ps.supplied FROM products AS pr
	                    LEFT JOIN (SELECT oi_tmp.product_id, SUM(oi_tmp.product_count) AS sold FROM order_items AS oi_tmp GROUP BY oi_tmp.product_id) AS oi ON oi.product_id = pr.id
	                    LEFT JOIN (SELECT ps_temp.product_id, SUM(ps_temp.amount) AS supplied FROM product_supplies AS ps_temp GROUP BY ps_temp.product_id) AS ps ON ps.product_id = pr.id
 	                    ;""")
    
    answ = db.execute(sql_query).all()
    return list(map(
        _process_product_db_answer_tuple,
        answ
    ))


def _process_product_db_answer_tuple(x):
    sold = x[2] if x[2] else 0
    supply = x[3] if x[3] else 0
    return ProductStorage(
        product_id=x[0],
        title=x[1],
        remaind=supply-sold
    )