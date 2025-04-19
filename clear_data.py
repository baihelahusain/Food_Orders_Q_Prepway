import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodsite.settings')
django.setup()

# Import models
from food.models import Item, Cart, Order, OrderItem
from django.contrib.auth.models import User
from django.db.models import Q

# Clear data
def clear_data():
    print("Clearing existing data...")
    
    # Delete all order items first (to avoid foreign key constraints)
    order_items_count = OrderItem.objects.all().count()
    OrderItem.objects.all().delete()
    print(f"Deleted {order_items_count} order items")
    
    # Delete all orders
    orders_count = Order.objects.all().count()
    Order.objects.all().delete()
    print(f"Deleted {orders_count} orders")
    
    # Delete all cart items
    cart_items_count = Cart.objects.all().count()
    Cart.objects.all().delete()
    print(f"Deleted {cart_items_count} cart items")
    
    # Delete all food items
    items_count = Item.objects.all().count()
    Item.objects.all().delete()
    print(f"Deleted {items_count} food items")
    
    print("All data cleared successfully!")

if __name__ == "__main__":
    clear_data() 