from fastapi import HTTPException, status
from fastapi.responses import FileResponse
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from sqlalchemy.sql import text
import csv
import uuid

from v1.auth.schema import ResponseSuccess
from v1.supplies.schema import SupplyResponse
from v1.supplies.controller import get_supplies_controller
from v1.orders.controller import get_orders_controller


async def get_report_supplies_controller(db: Session, date_from: date | None, date_to: date | None):
    supplies = await get_supplies_controller(db, date_from, date_to)

    file_path = f'tmp/{uuid.uuid4()}.csv'
    with open(file_path, 'w', newline='') as csvfile:
        field_names = ['supply_id', 'contractor_id', 
                        'contractor_title', 'product_id', 
                        'product_title', 'amount', 
                        'date']
        writer = csv.DictWriter(csvfile, fieldnames=field_names)

        writer.writeheader()
        for supply in supplies:
            writer.writerow({
                'supply_id': supply.id, 
                'contractor_id': supply.contractor.id, 
                'contractor_title': supply.contractor.title, 
                'product_id': supply.product.id, 
                'product_title': supply.product.title, 
                'amount': supply.amount, 
                'date': supply.date
            })

    return FileResponse(file_path, filename='report.csv', media_type='text/csv')


async def get_report_orders_controller(db: Session, is_paid: bool | None, is_deliver: bool | None, period_from: date | None, period_to: date | None):
    orders = await get_orders_controller(db, is_paid, is_deliver, period_from, period_to)

    file_path = f'tmp/{uuid.uuid4()}.csv'
    with open(file_path, 'w', newline='') as csvfile:
        field_names = [
            'order_id', 'order_number', 
            'order_date', 'order_note', 
            'delivery_terms', 'is_paid', 
            'id_deliver', 'customer_id', 
            'customer_title', 'customer_address',
            'customer_phone', 'customer_first_name', 'customer_last_name',
            'product_id', 'product_title', 
            'product_description', 'product_price',
            'product_count', 'product_package',
            'product_category']
        writer = csv.DictWriter(csvfile, fieldnames=field_names)

        writer.writeheader()
        for order in orders:
            for product in order.products:
                writer.writerow({
                    'order_id': order.id, 
                    'order_number': order.number, 
                    'order_date': order.date, 
                    'order_note': order.note, 
                    'delivery_terms': order.delivery_terms, 
                    'is_paid': 'Оплачен' if order.is_paid else 'Не оплачен', 
                    'id_deliver': 'Доставлен' if order.is_deliver else 'Не доставлен', 
                    'customer_id': order.customer.id, 
                    'customer_title': order.customer.title, 
                    'customer_address': order.customer.address,
                    'customer_phone': order.customer.phone, 
                    'customer_first_name': order.customer.first_name, 
                    'customer_last_name': order.customer.last_name,
                    'product_id': product.id, 
                    'product_title': product.title, 
                    'product_description': product.description, 
                    'product_price': product.price,
                    'product_count': product.count, 
                    'product_package': product.package,
                    'product_category': product.category.name
                })

    return FileResponse(file_path, filename='report.csv', media_type='text/csv')