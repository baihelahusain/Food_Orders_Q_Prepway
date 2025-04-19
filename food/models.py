from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Item(models.Model):
    CATEGORY_CHOICES = (
        ('fast_food', 'Fast Food'),
        ('main_course', 'Main Course'),
        ('drinks', 'Drinks'),
        ('sweet', 'Sweet'),
    )
    
    def __str__(self):
        return self.Item_name
    
    Item_name = models.CharField(max_length=200)
    Item_desc = models.TextField(max_length=500)
    Item_price = models.IntegerField()
    Item_img = models.CharField(max_length=1100, default="https://cdn-icons-png.flaticon.com/512/1377/1377194.png")
    item_image = models.ImageField(upload_to='food_images/', null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='fast_food')
    prep_time = models.CharField(max_length=50, blank=True, help_text="Preparation time (e.g., '30 minutes', '2 hours')")

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.quantity} of {self.item.Item_name}"
    
    @property
    def total_price(self):
        return self.quantity * self.item.Item_price

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    delivery_location = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    estimated_delivery_time = models.IntegerField(blank=True, null=True, help_text="Estimated delivery time in minutes")
    timer_start = models.DateTimeField(blank=True, null=True, help_text="When the delivery timer was started")
    
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} of {self.item.Item_name} in Order {self.order.id}"
