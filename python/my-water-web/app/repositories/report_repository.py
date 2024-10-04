import logging

from app.models import Category, Product, Order, OrderItems
from app import db
from sqlalchemy import func
from datetime import datetime

logger = logging.getLogger(__name__)

class ReportRepository:

    @staticmethod
    def report_sales(start_date, end_date):
        
        query = db.session.query(
            Category.name.label('categoria'),
            Product.name.label('produto'),
            func.sum(OrderItems.quantity).label('quantidade'),
            func.date(OrderItems.creation_date).label('data_venda')
        ).join(Product, Product.id == OrderItems.product_id
        ).join(Category, Category.id == Product.category_id
        ).group_by(Category.name, Product.name, func.date(OrderItems.creation_date)
        ).order_by(Category.name, Product.name, func.date(OrderItems.creation_date))

        if start_date and end_date:
            query = query.filter(OrderItems.creation_date.between(start_date, end_date))

        vendas = query.all() or list()
        return vendas

    

