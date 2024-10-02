import logging

from app.models import Order, OrderItems
from app import db

logger = logging.getLogger(__name__)

class OrderRepository:

    # Orders

    @staticmethod
    def add_order(order):
        logger.debug(f"Adicionando o pedido {order}")
        db.session.add(order)
        db.session.commit()

    @staticmethod
    def get_order_by_id(id):
        logger.debug(f"Consultando o pedido por id: {id}")
        return Order.query.get(id)

    @staticmethod
    def get_order_all():
        logger.debug("Listando todos os pedidos")
        return Order.query.all()

    @staticmethod
    def delete_order_by_id(id):
        logger.debug(f"Excluindo o pedido: {id}")

        order = Order.query.get(id)
        if order:
            db.session.delete(order)
            db.session.commit()

    # Orders Items

    @staticmethod
    def add_order_item(order_items):
        logger.debug(f"Adicionando o item do pedido {order_items}")
        db.session.add(order_items)
        db.session.commit()

    @staticmethod
    def get_order_item_by_id(id):
        logger.debug(f"Consultando o item do pedido por id: {id}")
        return OrderItems.query.get(id)

    @staticmethod
    def get_order_items_all():
        logger.debug("Listando todos os itens do pedidos")
        return OrderItems.query.all()

    @staticmethod
    def list_order_items_by_order(order_id):
        logger.debug("Listando os itens pelo pedido")
        return OrderItems.query.filter_by(order_id=order_id).all()

    @staticmethod
    def delete_order_item_by_id(id):
        logger.debug(f"Excluindo o pedido: {id}")

        order_item = OrderItems.query.get(id)
        if OrderItems:
            db.session.delete(order_item)
            db.session.commit()

