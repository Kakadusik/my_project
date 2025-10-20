from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from .services.product_management import ProductManagementService


@api_view(["GET"])
def product_list(request):
    """Получение списка доступных товаров"""
    try:
        products = ProductManagementService.get_available_products()
        product_data = [
            {
                "id": product.id,
                "name": product.name,
                "price": str(product.price),
                "stock": product.stock,
                "in_stock": product.is_in_stock(),
            }
            for product in products
        ]
        return Response({"products": product_data})
    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(["POST"])
def create_product(request):
    """Создание нового товара"""
    try:
        product = ProductManagementService.create_product(
            name=request.data["name"],
            price=request.data["price"],
            stock=request.data["stock"],
        )
        return Response(
            {
                "success": True,
                "product_id": product.id,
                "message": "Товар успешно создан",
            }
        )
    except ValidationError as e:
        return Response({"success": False, "error": str(e)}, status=400)
