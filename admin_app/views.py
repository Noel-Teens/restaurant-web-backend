from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from auth_app.models import User
from auth_app.serializers import UserSerializer
from restaurant_server.models import MenuItem, Review, OrderHistory, TableReservation
from restaurant_server.serializers import MenuItemSerializer, ReviewSerializer, TableReservationSerializer


def is_admin_user(user):
    """
    Check if user is admin/staff
    """
    return user.is_staff or user.is_superuser


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_users_list(request):
    """
    Get all registered users (admin only)
    """
    if not is_admin_user(request.user):
        return Response(
            {'error': 'Admin access required'},
            status=status.HTTP_403_FORBIDDEN
        )

    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_add_menu_item(request):
    """
    Add a new menu item (admin only)
    """
    if not is_admin_user(request.user):
        return Response(
            {'error': 'Admin access required'},
            status=status.HTTP_403_FORBIDDEN
        )

    serializer = MenuItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Menu item added successfully',
            'menu_item': serializer.data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def admin_delete_menu_item(request, menu_id):
    """
    Delete a menu item (admin only)
    """
    if not is_admin_user(request.user):
        return Response(
            {'error': 'Admin access required'},
            status=status.HTTP_403_FORBIDDEN
        )

    menu_item = get_object_or_404(MenuItem, id=menu_id)
    menu_item.delete()

    return Response({
        'message': 'Menu item deleted successfully'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_reviews_list(request):
    """
    Get all reviews (admin only)
    """
    if not is_admin_user(request.user):
        return Response(
            {'error': 'Admin access required'},
            status=status.HTTP_403_FORBIDDEN
        )

    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def admin_delete_review(request, review_id):
    """
    Delete a review (admin only)
    """
    if not is_admin_user(request.user):
        return Response(
            {'error': 'Admin access required'},
            status=status.HTTP_403_FORBIDDEN
        )

    review = get_object_or_404(Review, id=review_id)
    review.delete()

    return Response({
        'message': 'Review deleted successfully'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_menu_items(request):
    """
    Get all menu items including unavailable ones (admin only)
    """
    if not is_admin_user(request.user):
        return Response(
            {'error': 'Admin access required'},
            status=status.HTTP_403_FORBIDDEN
        )

    menu_items = MenuItem.objects.all()
    serializer = MenuItemSerializer(menu_items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def admin_user_details_or_delete(request, user_id):
    """
    GET: Get detailed information about a user including their associated data (admin only)
    DELETE: Delete a user and all associated data (admin only)
    """
    if not is_admin_user(request.user):
        return Response(
            {'error': 'Admin access required'},
            status=status.HTTP_403_FORBIDDEN
        )

    user = get_object_or_404(User, id=user_id)

    if request.method == 'GET':
        # Get counts of related data
        orders_count = user.orders.count()
        reservations_count = user.reservations.count()
        reviews_count = user.reviews.count()

        # Calculate total spent
        total_spent = sum(order.total_amount for order in user.orders.all())

        # Get pending and confirmed reservations count
        pending_reservations = user.reservations.filter(status='pending').count()
        confirmed_reservations = user.reservations.filter(status='confirmed').count()

        # Get recent orders (last 5)
        recent_orders = user.orders.all()[:5]
        recent_orders_data = []
        for order in recent_orders:
            recent_orders_data.append({
                'id': order.id,
                'order_date': order.order_date,
                'total_amount': order.total_amount,
                'status': order.status
            })

        # Get recent reservations (last 5)
        recent_reservations = user.reservations.all()[:5]
        recent_reservations_data = []
        for reservation in recent_reservations:
            recent_reservations_data.append({
                'id': reservation.id,
                'reservation_date': reservation.reservation_date,
                'reservation_time': reservation.reservation_time,
                'party_size': reservation.party_size,
                'status': reservation.status
            })

        return Response({
            'user': UserSerializer(user).data,
            'statistics': {
                'total_orders': orders_count,
                'total_spent': float(total_spent),
                'total_reviews': reviews_count,
                'total_reservations': reservations_count,
                'pending_reservations': pending_reservations,
                'confirmed_reservations': confirmed_reservations
            },
            'recent_orders': recent_orders_data,
            'recent_reservations': recent_reservations_data
        }, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        # Prevent admin from deleting their own account
        if user.id == request.user.id:
            return Response(
                {'error': 'Cannot delete your own account'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Count data before deletion for reporting
        orders_count = user.orders.count()
        order_items_count = sum(order.order_items.count() for order in user.orders.all())
        reservations_count = user.reservations.count()
        reviews_count = user.reviews.count()

        # Delete user (this will cascade delete all related data)
        user.delete()

        return Response({
            'message': 'User and all associated data deleted successfully',
            'deleted_data': {
                'orders': orders_count,
                'order_items': order_items_count,
                'reservations': reservations_count,
                'reviews': reviews_count
            }
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_bulk_delete_users(request):
    """
    Delete multiple users and all their associated data (admin only)
    Expects: {"user_ids": [1, 2, 3, ...]}
    """
    if not is_admin_user(request.user):
        return Response(
            {'error': 'Admin access required'},
            status=status.HTTP_403_FORBIDDEN
        )

    user_ids = request.data.get('user_ids', [])

    if not user_ids or not isinstance(user_ids, list):
        return Response(
            {'error': 'user_ids must be a non-empty list'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Prevent admin from deleting themselves
    if request.user.id in user_ids:
        return Response(
            {'error': 'Cannot delete your own account'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Get users to delete and validate they exist
    users_to_delete = User.objects.filter(id__in=user_ids)
    found_user_ids = list(users_to_delete.values_list('id', flat=True))
    missing_user_ids = [uid for uid in user_ids if uid not in found_user_ids]

    if missing_user_ids:
        return Response(
            {'error': f'Users with IDs {missing_user_ids} not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Collect statistics before deletion
    deletion_stats = []
    total_orders = 0
    total_reservations = 0
    total_reviews = 0

    for user in users_to_delete:
        orders_count = user.orders.count()
        reservations_count = user.reservations.count()
        reviews_count = user.reviews.count()

        deletion_stats.append({
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'orders_deleted': orders_count,
            'reservations_deleted': reservations_count,
            'reviews_deleted': reviews_count
        })

        total_orders += orders_count
        total_reservations += reservations_count
        total_reviews += reviews_count

    # Perform bulk deletion in transaction
    try:
        with transaction.atomic():
            deleted_count = users_to_delete.delete()[0]  # Returns (count, {model: count})

        return Response({
            'message': f'Successfully deleted {deleted_count} users and all associated data',
            'summary': {
                'users_deleted': deleted_count,
                'total_orders_deleted': total_orders,
                'total_reservations_deleted': total_reservations,
                'total_reviews_deleted': total_reviews
            },
            'details': deletion_stats
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': f'Failed to delete users: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_pending_reservations(request):
    """
    Get all pending reservations (admin only)
    """
    if not is_admin_user(request.user):
        return Response(
            {'error': 'Admin access required'},
            status=status.HTTP_403_FORBIDDEN
        )

    reservations = TableReservation.objects.filter(status='pending').order_by('reservation_date', 'reservation_time')
    serializer = TableReservationSerializer(reservations, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_all_reservations(request):
    """
    Get all reservations (admin only)
    """
    if not is_admin_user(request.user):
        return Response(
            {'error': 'Admin access required'},
            status=status.HTTP_403_FORBIDDEN
        )

    reservations = TableReservation.objects.all().order_by('-created_at')
    serializer = TableReservationSerializer(reservations, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_approve_reservation(request, reservation_id):
    """
    Approve a pending reservation (admin only)
    """
    if not is_admin_user(request.user):
        return Response(
            {'error': 'Admin access required'},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        reservation = get_object_or_404(TableReservation, id=reservation_id)

        # Get table number from request (optional)
        table_number = request.data.get('table_number')

        # Check if table is available at the requested time
        if table_number:
            existing_reservation = TableReservation.objects.filter(
                reservation_date=reservation.reservation_date,
                reservation_time=reservation.reservation_time,
                table_number=table_number,
                status__in=['confirmed', 'seated']
            ).exclude(id=reservation_id).first()

            if existing_reservation:
                return Response({
                    'error': f'Table {table_number} is already reserved for {reservation.reservation_date} at {reservation.reservation_time}'
                }, status=status.HTTP_400_BAD_REQUEST)

        # Update reservation status and assign table if provided
        reservation.status = 'confirmed'
        if table_number:
            reservation.table_number = table_number
        reservation.save()

        return Response({
            'message': 'Reservation approved successfully',
            'reservation': TableReservationSerializer(reservation).data
        }, status=status.HTTP_200_OK)

    except TableReservation.DoesNotExist:
        return Response({
            'error': 'Reservation not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_available_tables(request):
    """
    Get available tables for a specific date and time (admin only)
    """
    if not is_admin_user(request.user):
        return Response(
            {'error': 'Admin access required'},
            status=status.HTTP_403_FORBIDDEN
        )

    date = request.query_params.get('date')
    time = request.query_params.get('time')

    if not date or not time:
        return Response({
            'error': 'Date and time parameters are required'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Get all reserved tables for the specified date and time
    reserved_tables = TableReservation.objects.filter(
        reservation_date=date,
        reservation_time=time,
        status__in=['confirmed', 'seated']
    ).values_list('table_number', flat=True)

    # Assume we have tables 1-20 (you can adjust this based on your restaurant)
    all_tables = list(range(1, 21))
    available_tables = [table for table in all_tables if table not in reserved_tables]

    return Response({
        'date': date,
        'time': time,
        'available_tables': available_tables,
        'reserved_tables': list(reserved_tables)
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_reject_reservation(request, reservation_id):
    """
    Reject a pending reservation (admin only)
    """
    if not is_admin_user(request.user):
        return Response(
            {'error': 'Admin access required'},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        reservation = get_object_or_404(TableReservation, id=reservation_id)

        # Update reservation status to cancelled
        reservation.status = 'cancelled'
        reservation.save()

        return Response({
            'message': 'Reservation rejected successfully',
            'reservation': TableReservationSerializer(reservation).data
        }, status=status.HTTP_200_OK)

    except TableReservation.DoesNotExist:
        return Response({
            'error': 'Reservation not found'
        }, status=status.HTTP_404_NOT_FOUND)
