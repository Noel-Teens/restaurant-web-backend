from rest_framework import serializers
from .models import MenuItem, OrderHistory, OrderItem, TableReservation, Review
from auth_app.serializers import UserSerializer


class MenuItemSerializer(serializers.ModelSerializer):
    """
    Serializer for MenuItem model
    """
    class Meta:
        model = MenuItem
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderItem model
    """
    menu_item = MenuItemSerializer(read_only=True)
    menu_item_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = OrderItem
        fields = ('id', 'menu_item', 'menu_item_id', 'quantity', 'price_at_time')
        read_only_fields = ('price_at_time',)


class OrderHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for OrderHistory model
    """
    user = UserSerializer(read_only=True)
    order_items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)
    items = serializers.ListField(child=serializers.DictField(), write_only=True)
    
    class Meta:
        model = OrderHistory
        fields = ('id', 'user', 'order_date', 'total_amount', 'status', 
                 'special_instructions', 'order_items', 'items')
        read_only_fields = ('id', 'user', 'order_date', 'total_amount')
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = OrderHistory.objects.create(**validated_data)
        
        total_amount = 0
        for item_data in items_data:
            menu_item = MenuItem.objects.get(id=item_data['menu_item_id'])
            quantity = item_data['quantity']
            price_at_time = menu_item.food_price
            
            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=quantity,
                price_at_time=price_at_time
            )
            total_amount += price_at_time * quantity
        
        order.total_amount = total_amount
        order.save()
        return order


class TableReservationSerializer(serializers.ModelSerializer):
    """
    Serializer for TableReservation model
    """
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = TableReservation
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'table_number')
    
    def validate(self, attrs):
        # Check if the reservation date and time is not in the past
        from datetime import datetime, date, time
        reservation_datetime = datetime.combine(
            attrs['reservation_date'], 
            attrs['reservation_time']
        )
        if reservation_datetime < datetime.now():
            raise serializers.ValidationError(
                "Cannot make reservations for past dates and times"
            )
        return attrs


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for Review model
    """
    user = UserSerializer(read_only=True)
    order_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Review
        fields = ('id', 'order_id', 'user', 'stars', 'description', 
                 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')
    
    def validate_order_id(self, value):
        try:
            order = OrderHistory.objects.get(id=value, user=self.context['request'].user)
            if hasattr(order, 'review'):
                raise serializers.ValidationError("This order already has a review")
            return value
        except OrderHistory.DoesNotExist:
            raise serializers.ValidationError("Order not found or doesn't belong to you")
    
    def create(self, validated_data):
        order_id = validated_data.pop('order_id')
        order = OrderHistory.objects.get(id=order_id)
        review = Review.objects.create(order=order, **validated_data)
        return review
