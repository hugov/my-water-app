import logging

from app.models import Category, Product, Order, OrderItems
from app import db
from sqlalchemy import func
from datetime import datetime

logger = logging.getLogger(__name__)

class ReportRepository:

    @staticmethod
    def report_sales(category_filter, product_filter, start_date, end_date):
        
        query = db.session.query(
            Category.name.label('categoria'),
            Product.name.label('produto'),
            func.sum(OrderItems.quantity).label('quantidade'),
            func.date(OrderItems.creation_date).label('data_venda')
        ).join(Product, Product.id == OrderItems.product_id
        ).join(Category, Category.id == Product.category_id
        ).group_by(Category.name, Product.name, func.date(OrderItems.creation_date)
        ).order_by(Category.name, Product.name, func.date(OrderItems.creation_date))

        # Filtros
        if category_filter:
            query = query.filter(Category.name.like(f'%{category_filter}%'))
        if product_filter:
            query = query.filter(Product.name.like(f'%{product_filter}%'))
        if start_date and end_date:
            query = query.filter(OrderItems.creation_date.between(start_date, end_date))

        vendas = query.all()

    

