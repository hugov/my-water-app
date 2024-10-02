import logging

from app.repositories.order_repository import OrderRepository

logger = logging.getLogger(__name__)

class OrderService:

    # Order

    @staticmethod
    def create_order(order):
        _order = order
        OrderRepository.add_order(_order)
        return _order

    @staticmethod
    def get_order(id):
        return OrderRepository.get_order_by_id(id)

    @staticmethod
    def list_order():
        return OrderRepository.get_order_all()

    @staticmethod
    def delete_order(id):
        return OrderRepository.delete_order_by_id(id)

    # Order Item

    @staticmethod
    def create_order_item(order):
        _order = order
        OrderRepository.add_order_item(_order)
        return _order

    @staticmethod
    def get_order_item(id):
        return OrderRepository.get_order_item_by_id(id)

    @staticmethod
    def list_order_items():
        return OrderRepository.get_order_items_all()

    @staticmethod
    def list_order_items_by_order(order_id):
        return OrderRepository.list_order_items_by_order(order_id)

    @staticmethod
    def delete_order_item(id):
        return OrderRepository.delete_order_item_by_id(id)