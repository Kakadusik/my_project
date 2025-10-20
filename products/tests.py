from django.test import TestCase
from products.models import Product
from products.services.product_management import ProductManagementService


class ProductModelTest(TestCase):
    """Тесты для модели Product"""

    def test_product_creation(self):
        """Тест создания товара"""
        product = Product.objects.create(name="Тестовый товар", price=100, stock=10)
        self.assertEqual(product.name, "Тестовый товар")
        self.assertTrue(product.is_in_stock())

    def test_reduce_stock(self):
        """Тест списания товара"""
        product = Product.objects.create(name="Товар", price=50, stock=5)

        # Успешное списание
        result = product.reduce_stock(3)
        self.assertTrue(result)
        self.assertEqual(product.stock, 2)

        # Неудачное списание (недостаточно товара)
        result = product.reduce_stock(5)
        self.assertFalse(result)
        self.assertEqual(product.stock, 2)  # Остаток не изменился


class ProductServiceTest(TestCase):
    """Тесты для сервиса управления товарами"""

    def test_create_product_success(self):
        """Тест успешного создания товара через сервис"""
        product = ProductManagementService.create_product(
            name="Новый товар", price=200, stock=15
        )
        self.assertEqual(product.name, "Новый товар")
        self.assertEqual(product.price, 200)
        self.assertEqual(product.stock, 15)

    def test_create_product_invalid_price(self):
        """Тест создания товара с неверной ценой"""
        with self.assertRaises(Exception) as context:
            ProductManagementService.create_product("Товар", -100, 10)
        self.assertIn("Цена должна быть положительной", str(context.exception))
