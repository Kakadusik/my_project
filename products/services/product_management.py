from django.core.exceptions import ValidationError
from products.models import Product


class ProductManagementService:
    """
    Сервис для управления товарами
    """

    @staticmethod
    def create_product(name, price, stock):
        """Создание нового товара с проверками"""
        if price <= 0:
            raise ValidationError("Цена должна быть положительной")

        if stock < 0:
            raise ValidationError("Количество не может быть отрицательным")

        product = Product.objects.create(name=name, price=price, stock=stock)
        return product

    @staticmethod
    def update_product_price(product_id, new_price):
        """Обновление цены товара"""
        if new_price <= 0:
            raise ValidationError("Цена должна быть положительной")

        try:
            product = Product.objects.get(id=product_id)
            product.price = new_price
            product.save()
            return product
        except Product.DoesNotExist:
            raise ValidationError("Товар не найден")

    @staticmethod
    def get_available_products():
        """Получение всех доступных товаров"""
        return Product.objects.filter(is_active=True, stock__gt=0)

    @staticmethod
    def apply_bulk_discount(product_ids, discount_percent):
        """Применение скидки к нескольким товарам"""
        if discount_percent <= 0 or discount_percent >= 100:
            raise ValidationError("Скидка должна быть между 0 и 100%")

        products = Product.objects.filter(id__in=product_ids)
        updated_products = []

        for product in products:
            # Здесь может быть сложная логика применения скидки
            product.price = product.get_discounted_price(discount_percent)
            product.save()
            updated_products.append(product)

        return updated_products
