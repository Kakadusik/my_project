from django.test import TestCase
from django.contrib.auth.models import User
from products.models import Product
from orders.services.order_creation import OrderCreationService


class OrderServiceTest(TestCase):
    """Тесты для сервиса создания заказов"""

    def setUp(self):
        # Создаем тестовые данные
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.product1 = Product.objects.create(name="Товар 1", price=100, stock=10)
        self.product2 = Product.objects.create(name="Товар 2", price=200, stock=5)

    def test_create_order_success(self):
        """Тест успешного создания заказа"""
        order = OrderCreationService.create_order(
            user=self.user,
            product_quantities=[
                {"product_id": self.product1.id, "quantity": 2},
                {"product_id": self.product2.id, "quantity": 1},
            ],
        )

        self.assertEqual(order.user, self.user)
        self.assertEqual(order.total_amount, 400)  # 2*100 + 1*200
        self.assertEqual(order.status, "pending")

        # Проверяем, что товары списались
        self.product1.refresh_from_db()
        self.product2.refresh_from_db()
        self.assertEqual(self.product1.stock, 8)
        self.assertEqual(self.product2.stock, 4)

    def test_create_order_insufficient_stock(self):
        """Тест создания заказа при недостатке товара"""
        with self.assertRaises(Exception) as context:
            OrderCreationService.create_order(
                user=self.user,
                product_quantities=[
                    {"product_id": self.product1.id, "quantity": 15}  # Больше чем есть
                ],
            )
        self.assertIn("Недостаточно товара", str(context.exception))
