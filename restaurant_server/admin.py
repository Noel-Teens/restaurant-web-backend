from django.contrib import admin
from .models import MenuItem, OrderHistory, OrderItem, TableReservation, Review


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('food_name', 'food_price', 'is_available', 'created_at')
    list_filter = ('is_available', 'created_at')
    search_fields = ('food_name', 'food_description')
    list_editable = ('food_price', 'is_available')
    ordering = ('food_name',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('price_at_time',)


@admin.register(OrderHistory)
class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_date', 'total_amount', 'status')
    list_filter = ('status', 'order_date')
    search_fields = ('user__username', 'user__email')
    list_editable = ('status',)
    ordering = ('-order_date',)
    inlines = [OrderItemInline]
    readonly_fields = ('order_date', 'total_amount')


@admin.register(TableReservation)
class TableReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'reservation_date', 'reservation_time', 'party_size', 'status', 'table_number')
    list_filter = ('status', 'reservation_date', 'party_size')
    search_fields = ('user__username', 'user__email')
    list_editable = ('status', 'table_number')
    ordering = ('reservation_date', 'reservation_time')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'stars', 'created_at')
    list_filter = ('stars', 'created_at')
    search_fields = ('user__username', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
