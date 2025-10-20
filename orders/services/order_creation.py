from django.core.exceptions import ValidationError
from django.db import transaction
from orders.models import Order, OrderItem
from products.models import Product


class OrderCreationService:
    """
    Сервис для создания заказов
    """

    @staticmethod
    @transaction.atomic
    def create_order(user, product_quantities):
        """
        Создание заказа с проверкой бизнес-правил
        product_quantities: список словарей [{'product_id': 1, 'quantity': 2}]
        """
        if not product_quantities:
            raise ValidationError("Заказ не может быть пустым")

        # Проверяем все товары перед созданием заказа
        total_amount = 0
        order_items_data = []

        for item in product_quantities:
            product_id = item["product_id"]
            quantity = item["quantity"]

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                raise ValidationError(f"Товар с ID {product_id} не найден")

            # Используем метод модели для проверки
            if not product.is_in_stock():
                raise ValidationError(f"Товар '{product.name}' отсутствует на складе")

            if product.stock < quantity:
                raise ValidationError(
                    f"Недостаточно товара '{product.name}' на складе. Доступно: {product.stock}"
                )

            # Рассчитываем стоимость
            item_total = product.price * quantity
            total_amount += item_total

            order_items_data.append(
                {"product": product, "quantity": quantity, "price": product.price}
            )

        # Создаем заказ
        order = Order.objects.create(
            user=user, total_amount=total_amount, status="pending"
        )

        # Создаем элементы заказа и списываем товары со склада
        for item_data in order_items_data:
            OrderItem.objects.create(
                order=order,
                product=item_data["product"],
                quantity=item_data["quantity"],
                price=item_data["price"],
            )

            # Списание товара со склада
            item_data["product"].reduce_stock(item_data["quantity"])

        # Здесь могла бы быть дополнительная логика:
        # - Отправка email уведомления
        # - Создание уведомления для администратора
        # - Интеграция с системой доставки

        return order

    @staticmethod
    @transaction.atomic
    def cancel_order(order_id):
        """Отмена заказа и возврат товаров на склад"""
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise ValidationError("Заказ не найден")

        if order.status == "cancelled":
            raise ValidationError("Заказ уже отменен")

        # Возвращаем товары на склад
        for item in order.items.all():
            item.product.increase_stock(item.quantity)

        order.status = "cancelled"
        order.save()

        return order
