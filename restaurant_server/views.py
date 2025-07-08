from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import MenuItem, OrderHistory, TableReservation, Review
from .serializers import (
    MenuItemSerializer, OrderHistorySerializer,
    TableReservationSerializer, ReviewSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['GET'])
@permission_classes([AllowAny])
def menu_list(request):
    """
    Get all available menu items
    """
    menu_items = MenuItem.objects.filter(is_available=True)
    serializer = MenuItemSerializer(menu_items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_reservation(request):
    """
    Create a new table reservation
    """
    serializer = TableReservationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({
            'message': 'Reservation created successfully',
            'reservation': serializer.data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_reservations(request):
    """
    Get user's reservations
    """
    reservations = TableReservation.objects.filter(user=request.user)
    serializer = TableReservationSerializer(reservations, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    """
    Create a new order
    """
    serializer = OrderHistorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({
            'message': 'Order placed successfully',
            'order': serializer.data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_orders(request):
    """
    Get user's order history
    """
    orders = OrderHistory.objects.filter(user=request.user)
    serializer = OrderHistorySerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request):
    """
    Create a new review for an order
    """
    serializer = ReviewSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({
            'message': 'Review submitted successfully',
            'review': serializer.data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def reviews_list(request):
    """
    Get all reviews (public endpoint)
    """
    reviews = Review.objects.all()
    paginator = StandardResultsSetPagination()
    result_page = paginator.paginate_queryset(reviews, request)
    serializer = ReviewSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout_cart(request):
    """
    Checkout cart items and create order with 'delivered' status
    """
    from .models import OrderItem

    # Get items from request
    items_data = request.data.get('items', [])
    special_instructions = request.data.get('special_instructions', '')

    if not items_data:
        return Response({
            'error': 'No items provided for checkout'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Calculate total amount
    total_amount = 0
    for item_data in items_data:
        try:
            menu_item = MenuItem.objects.get(id=item_data['menu_item_id'])
            quantity = item_data['quantity']
            total_amount += menu_item.food_price * quantity
        except MenuItem.DoesNotExist:
            return Response({
                'error': f"Menu item with id {item_data['menu_item_id']} not found"
            }, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({
                'error': 'Invalid item data format'
            }, status=status.HTTP_400_BAD_REQUEST)

    # Create order with calculated total and delivered status
    order = OrderHistory.objects.create(
        user=request.user,
        total_amount=total_amount,
        status='delivered',
        special_instructions=special_instructions
    )

    # Create order items
    for item_data in items_data:
        menu_item = MenuItem.objects.get(id=item_data['menu_item_id'])
        OrderItem.objects.create(
            order=order,
            menu_item=menu_item,
            quantity=item_data['quantity'],
            price_at_time=menu_item.food_price
        )

    return Response({
        'message': 'Order placed and delivered successfully',
        'order': OrderHistorySerializer(order).data
    }, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    """
    Update user's profile information (first_name, last_name)
    """
    user = request.user

    # Get the data from request
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')

    # Validate that at least one field is provided
    if first_name is None and last_name is None:
        return Response({
            'error': 'At least one field (first_name or last_name) must be provided'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Update fields if provided
    if first_name is not None:
        user.first_name = first_name

    if last_name is not None:
        user.last_name = last_name

    # Save the user
    user.save()

    # Import UserSerializer here to avoid circular imports
    from auth_app.serializers import UserSerializer

    return Response({
        'message': 'Profile updated successfully',
        'user': UserSerializer(user).data
    }, status=status.HTTP_200_OK)

