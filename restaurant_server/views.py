from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
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
