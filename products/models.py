from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    stock = models.IntegerField(verbose_name="Количество на складе")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name

    # Простая логика, относящаяся только к этой модели
    def is_in_stock(self):
        """Проверяет, есть ли товар в наличии"""
        return self.stock > 0

    def reduce_stock(self, quantity):
        """Уменьшает количество товара на складе"""
        if self.stock >= quantity:
            self.stock -= quantity
            self.save()
            return True
        return False

    def increase_stock(self, quantity):
        """Увеличивает количество товара на складе"""
        self.stock += quantity
        self.save()
        return True

    def get_discounted_price(self, discount_percent=10):
        """Возвращает цену со скидкой"""
        return self.price * (1 - discount_percent / 100)
