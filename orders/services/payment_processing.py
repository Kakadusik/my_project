from django.core.exceptions import ValidationError
from orders.models import Order


class PaymentProcessingService:
    """
    Сервис для обработки платежей
    """

    @staticmethod
    def process_payment(order_id, payment_method="card"):
        """Обработка платежа для заказа"""
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise ValidationError("Заказ не найден")

        if order.status != "pending":
            raise ValidationError("Нельзя оплатить этот заказ")

        # Имитация обработки платежа
        # В реальном проекте здесь была бы интеграция с платежной системой
        if payment_method not in ["card", "cash", "online"]:
            raise ValidationError("Неверный способ оплаты")

        # Имитация успешной оплаты
        order.status = "processing"
        order.save()

        # Здесь могла бы быть логика:
        # - Интеграция с банком
        # - Создание чека
        # - Отправка подтверждения оплаты

        return {
            "success": True,
            "order_id": order.id,
            "amount": order.total_amount,
            "payment_method": payment_method,
        }
