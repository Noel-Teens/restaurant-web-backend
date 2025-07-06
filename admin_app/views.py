from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from auth_app.models import User
from auth_app.serializers import UserSerializer
from restaurant_server.models import MenuItem, Review
from restaurant_server.serializers import MenuItemSerializer, ReviewSerializer


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
