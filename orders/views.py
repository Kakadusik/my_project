from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from .services.order_creation import OrderCreationService
from .services.payment_processing import PaymentProcessingService

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    """Создание нового заказа"""
    try:
        order = OrderCreationService.create_order(
            user=request.user,
            product_quantities=request.data['products']
        )
        return Response({
            'success': True,
            'order_id': order.id,
            'total_amount': str(order.total_amount),
            'status': order.status
        })
    except ValidationError as e:
        return Response({'success': False, 'error': str(e)}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def process_payment(request):
    """Обработка платежа для заказа"""
    try:
        result = PaymentProcessingService.process_payment(
            order_id=request.data['order_id'],
            payment_method=request.data.get('payment_method', 'card')
        )
        return Response(result)
    except ValidationError as e:
        return Response({'success': False, 'error': str(e)}, status=400)