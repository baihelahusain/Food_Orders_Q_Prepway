from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Item, Cart, Order, OrderItem
from django.template import loader
from .forms import ItemForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.db.models import Sum, F, Count
from decimal import Decimal

# Function to check if user is a superuser
def is_superuser(user):
    return user.is_superuser

# Create your views here.
def index(request):
    # Get selected category from request, if any
    selected_category = request.GET.get('category', None)
    
    # Get all items
    all_items = Item.objects.all()
    
    # Filter items by category if selected
    if selected_category:
        filtered_items = all_items.filter(category=selected_category)
    else:
        filtered_items = all_items
    
    # Create a dictionary of categories for the template
    categories = dict(Item.CATEGORY_CHOICES)
    
    # Create a dictionary to organize items by category
    categorized_items = {}
    for cat_key, cat_name in Item.CATEGORY_CHOICES:
        cat_items = all_items.filter(category=cat_key)
        if cat_items.exists():
            categorized_items[cat_key] = {
                'name': cat_name,
                'items': cat_items
            }
    
    # Debug information
    print(f"Categories available: {categories}")
    print(f"Selected category: {selected_category}")
    print(f"Items filtered: {filtered_items.count()}")
    print(f"Categorized items: {[key for key in categorized_items.keys()]}")
    
    context = {
        'item_list': filtered_items,
        'categorized_items': categorized_items,
        'categories': categories,
        'selected_category': selected_category
    }
    
    return render(request, "food/index.html", context)
       
def item(request):
    return HttpResponse("HEllo")

def detail(request, item_id):
    item = Item.objects.get(pk=item_id)
    
    # Determine which image to use: uploaded image or URL
    if item.item_image and item.item_image.url:
        item_image = item.item_image.url
    else:
        item_image = item.Item_img
        
    context = {
        'item': item,
        'item_image': item_image
    }
    return render(request, "food/detail.html", context)

@login_required
@user_passes_test(is_superuser)
def create_item(request):
    if not request.user.is_superuser:
        raise PermissionDenied("You don't have permission to add items")
    
    form = ItemForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Food item added successfully!")
        return redirect('food:index')
    return render(request, 'food/item-form.html', {'form': form})

@login_required
@user_passes_test(is_superuser)
def update_item(request,id):
    if not request.user.is_superuser:
        raise PermissionDenied("You don't have permission to update items")
    
    item = Item.objects.get(id=id)
    form = ItemForm(request.POST or None, request.FILES or None, instance=item)
    if form.is_valid():
        form.save()
        messages.success(request, "Food item updated successfully!")
        return redirect('food:index')
    return render(request, 'food/item-form.html', {'form': form, 'item': item})

@login_required
@user_passes_test(is_superuser)
def delete_item(request, id):
    if not request.user.is_superuser:
        raise PermissionDenied("You don't have permission to delete items")
    
    item = Item.objects.get(id=id)
    if request.method == 'POST':
        item.delete()
        return redirect('food:index')
    return render(request, 'food/item-delete.html', {'item': item})

# Cart functionality
@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, item=item)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        
    messages.success(request, f"{item.Item_name} added to your cart!")
    return redirect('food:index')

@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total
    }
    return render(request, 'food/cart.html', context)

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(Cart, user=request.user, item_id=item_id)
    action = request.POST.get('action')
    
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            cart_item.delete()
            messages.info(request, f"{cart_item.item.Item_name} removed from cart")
            return redirect('food:view_cart')
    
    cart_item.save()
    return redirect('food:view_cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(Cart, user=request.user, item_id=item_id)
    cart_item.delete()
    messages.info(request, f"{cart_item.item.Item_name} removed from cart")
    return redirect('food:view_cart')

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    
    if not cart_items.exists():
        messages.warning(request, "Your cart is empty!")
        return redirect('food:view_cart')
    
    total_price = sum(item.total_price for item in cart_items)
    
    if request.method == 'POST':
        # Get form data
        contact_number = request.POST.get('contact_number')
        delivery_location = request.POST.get('delivery_location')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        payment_method = request.POST.get('payment_method')
        
        # Create new order
        order = Order.objects.create(
            user=request.user,
            total_price=Decimal(total_price),
            contact_number=contact_number,
            delivery_location=delivery_location
        )
        
        # Save map coordinates if provided
        if latitude and longitude:
            order.latitude = latitude
            order.longitude = longitude
            order.save()
        
        # Create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                item=cart_item.item,
                quantity=cart_item.quantity,
                price=Decimal(cart_item.item.Item_price)
            )
        
        # Update user profile with delivery address if provided
        if delivery_location and hasattr(request.user, 'profile'):
            profile = request.user.profile
            profile.location = delivery_location
            profile.save()
        
        # Clear the cart
        cart_items.delete()
        
        messages.success(request, "Your order has been placed successfully!")
        return redirect('food:order_confirmation', order_id=order.id)
    
    context = {
        'cart_items': cart_items,
        'total': total_price
    }
    return render(request, 'food/checkout.html', context)

@login_required
@user_passes_test(is_superuser)
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    
    # Calculate remaining time for timer (if set)
    time_remaining = None
    expiration_timestamp = None
    if order.estimated_delivery_time:
        import datetime
        from django.utils import timezone
        
        # If there's no timer_start, initialize it now
        if not order.timer_start:
            order.timer_start = timezone.now()
            order.save()
            
        # Calculate when timer expires (delivery time)
        expiration_time = order.timer_start + datetime.timedelta(minutes=order.estimated_delivery_time)
        expiration_timestamp = int(expiration_time.timestamp() * 1000)  # Convert to milliseconds for JS
        
        # Calculate remaining time in seconds
        now = timezone.now()
        time_remaining = max(0, int((expiration_time - now).total_seconds()))
    
    if request.method == 'POST':
        if 'status' in request.POST:
            status = request.POST.get('status')
            if status in dict(Order.STATUS_CHOICES).keys():
                order.status = status
                order.save()
                messages.success(request, f"Order status updated to {order.get_status_display()}")
        
        if 'estimated_delivery_time' in request.POST:
            try:
                estimated_time = request.POST.get('estimated_delivery_time')
                if estimated_time:
                    # Reset timer when delivery time is updated
                    from django.utils import timezone
                    order.estimated_delivery_time = int(estimated_time)
                    order.timer_start = timezone.now()  # Reset the timer
                    order.save()
                    messages.success(request, f"Delivery time updated to {order.estimated_delivery_time} minutes")
                else:
                    order.estimated_delivery_time = None
                    order.timer_start = None
                    order.save()
                    messages.success(request, "Delivery time estimate removed")
            except ValueError:
                messages.error(request, "Please enter a valid number for delivery time")
        
        if 'delete_order' in request.POST and request.user.is_superuser:
            # Check if order status is delivered or cancelled
            if order.status == 'delivered' or order.status == 'cancelled':
                # Delete related order items first to avoid foreign key constraints
                OrderItem.objects.filter(order=order).delete()
                order.delete()
                messages.success(request, "Order has been removed from the system")
                return redirect('food:all_orders')
            else:
                messages.error(request, "Only delivered or cancelled orders can be removed")
    
    context = {
        'order': order,
        'order_items': order_items,
        'status_choices': Order.STATUS_CHOICES,
        'time_remaining': time_remaining,
        'expiration_timestamp': expiration_timestamp
    }
    return render(request, 'food/order_detail.html', context)

@login_required
@user_passes_test(is_superuser)
def delete_order(request, order_id):
    if request.method == 'POST' and request.user.is_superuser:
        order = get_object_or_404(Order, id=order_id)
        
        # Only allow deletion of delivered or cancelled orders
        if order.status in ['delivered', 'cancelled']:
            # Delete related order items first to avoid foreign key constraints
            OrderItem.objects.filter(order=order).delete()
            order.delete()
            messages.success(request, "Order has been removed from the system")
        else:
            messages.error(request, "Only delivered or cancelled orders can be removed")
            
    return redirect('food:all_orders')

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)
    
    # Calculate remaining time for timer (if set)
    time_remaining = None
    expiration_timestamp = None
    if order.estimated_delivery_time:
        import datetime
        from django.utils import timezone
        
        # Calculate when timer expires (delivery time)
        if order.timer_start:
            expiration_time = order.timer_start + datetime.timedelta(minutes=order.estimated_delivery_time)
            expiration_timestamp = int(expiration_time.timestamp() * 1000)  # Convert to milliseconds for JS
            
            # Calculate remaining time in seconds
            now = timezone.now()
            time_remaining = max(0, int((expiration_time - now).total_seconds()))
    
    context = {
        'order': order,
        'order_items': order_items,
        'time_remaining': time_remaining,
        'expiration_timestamp': expiration_timestamp
    }
    return render(request, 'food/order_confirmation.html', context)

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # Calculate remaining times for all orders with timers
    from django.utils import timezone
    import datetime
    
    for order in orders:
        if order.estimated_delivery_time and order.timer_start:
            expiration_time = order.timer_start + datetime.timedelta(minutes=order.estimated_delivery_time)
            order.expiration_timestamp = int(expiration_time.timestamp() * 1000)
            
            # Calculate remaining time in seconds
            now = timezone.now()
            order.time_remaining = max(0, int((expiration_time - now).total_seconds()))
    
    context = {
        'orders': orders
    }
    return render(request, 'food/order_history.html', context)

# Superuser order management views
@login_required
@user_passes_test(is_superuser)
def all_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    
    context = {
        'orders': orders
    }
    return render(request, 'food/all_orders.html', context)