from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class MenuItem(models.Model):
    """
    Model representing a menu item in the restaurant
    """
    food_image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    food_name = models.CharField(max_length=100)
    food_description = models.TextField()
    food_price = models.FloatField(validators=[MinValueValidator(0.01)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.food_name

    class Meta:
        ordering = ['food_name']


class OrderHistory(models.Model):
    """
    Model representing order history for users
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    menu_items = models.ManyToManyField(MenuItem, through='OrderItem')
    total_amount = models.FloatField(validators=[MinValueValidator(0.01)])
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    special_instructions = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username} on {self.order_date.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['-order_date']
        verbose_name_plural = "Order Histories"


class OrderItem(models.Model):
    """
    Through model for OrderHistory and MenuItem relationship
    """
    order = models.ForeignKey(OrderHistory, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price_at_time = models.FloatField(validators=[MinValueValidator(0.01)])

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.food_name} in Order #{self.order.id}"


class TableReservation(models.Model):
    """
    Model representing table reservations
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    party_size = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    table_number = models.PositiveIntegerField(blank=True, null=True)
    special_requests = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('seated', 'Seated'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation for {self.user.username} on {self.reservation_date} at {self.reservation_time}"

    class Meta:
        ordering = ['reservation_date', 'reservation_time']
        unique_together = ['reservation_date', 'reservation_time', 'table_number']


class Review(models.Model):
    """
    Model representing customer reviews linked to orders
    """
    order = models.OneToOneField(OrderHistory, on_delete=models.CASCADE, related_name='review')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    stars = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.stars}-star review by {self.user.username} for Order #{self.order.id}"

    class Meta:
        ordering = ['-created_at']
