📋 О проекте

Учебный проект на Django, демонстрирующий правильную организацию бизнес-логики с использованием сервисного слоя. Проект представляет собой упрощенную систему интернет-магазина с товарами, заказами и пользователями.

🏗️ Архитектура

Проект реализован с четким разделением ответственности:

    Модели (Models) - содержат только логику, связанную с данными

    Сервисы (Services) - инкапсулируют сложную бизнес-логику

    Представления (Views) - обрабатывают HTTP-запросы и ответы

📁 Структура проекта

```text
my_project/
├── products/                 # Приложение товаров
│   ├── services/
│   │   └── product_management.py
│   ├── models.py
│   ├── views.py
│   └── tests.py
├── orders/                  # Приложение заказов
│   ├── services/
│   │   ├── order_creation.py
│   │   └── payment_processing.py
│   ├── models.py
│   ├── views.py
│   └── tests.py
├── users/                   # Приложение пользователей
│   ├── services/
│   │   └── user_registration.py
│   └── models.py
├── my_project/              # Настройки проекта
└── manage.py
```

🚀 Быстрый старт
Предварительные требования

    Python 3.8+

    Django 4.2+

    Django REST Framework

Установка и запуск

    Клонируйте репозиторий:

```bash

git clone <url-репозитория>
cd my_project
```

Создайте виртуальное окружение:

```bash

python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

Установите зависимости:

```bash

pip install -r requirements.txt
```
Примените миграции:

```bash

python manage.py makemigrations
python manage.py migrate
```
Создайте суперпользователя:

```bash

python manage.py createsuperuser
```
Запустите сервер:

```bash

python manage.py runserver
```

📚 API Endpoints

Товары
```
    GET /api/products/ - список товаров

    POST /api/products/create/ - создание товара
```

Заказы

```
    POST /api/orders/create/ - создание заказа

    POST /api/orders/payment/ - обработка платежа

```

🧪 Тестирование

Проект включает примеры unit-тестов для моделей и сервисов:
```bash

# Запуск всех тестов
python manage.py test

# Запуск тестов конкретного приложения
python manage.py test products
python manage.py test orders
```

🔧 Ключевые особенности
1. Сервисный слой

Бизнес-логика вынесена в отдельные сервисные классы:
```python

# Пример сервиса
class OrderCreationService:
    @staticmethod
    @transaction.atomic
    def create_order(user, product_quantities):
        # Сложная бизнес-логика создания заказа
        pass
```

2. Чистые модели

Модели содержат только методы, связанные с данными:
```python

class Product(models.Model):
    def is_in_stock(self):
        return self.stock > 0
    
    def reduce_stock(self, quantity):
        # Простая логика работы с данными модели
        pass
```

3. Простое тестирование

Сервисный слой позволяет легко тестировать бизнес-логику:
```python

def test_create_order_success(self):
    order = OrderCreationService.create_order(user, products)
    self.assertEqual(order.status, 'pending')
```
