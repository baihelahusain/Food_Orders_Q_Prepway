from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.db.models import Sum, Count
from food.models import Order
 
# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # Automatically log in the user after registration
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profilepage(request):
    # Check if user has a profile, create one if not
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, 
                                  request.FILES, 
                                  instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)
    
    # Get order statistics
    orders = Order.objects.filter(user=request.user)
    total_orders = orders.count()
    total_spent = orders.aggregate(total=Sum('total_price'))['total'] or 0
    
    # For superusers, show the overall order statistics
    if request.user.is_superuser:
        all_orders = Order.objects.all()
        delivered_orders = all_orders.filter(status='delivered')
        total_earnings = delivered_orders.aggregate(total=Sum('total_price'))['total'] or 0
        total_customers = delivered_orders.values('user').annotate(count=Count('user')).count()
        
        # Get user details who ordered
        top_customers = Order.objects.filter(status='delivered').values(
            'user__username', 'user__email'
        ).annotate(
            order_count=Count('id'),
            total_spent=Sum('total_price')
        ).order_by('-total_spent')[:5]
        
        context = {
            'u_form': u_form,
            'p_form': p_form,
            'orders': orders,
            'total_orders': total_orders,
            'total_spent': total_spent,
            'is_superuser': True,
            'total_earnings': total_earnings,
            'total_customers': total_customers,
            'top_customers': top_customers
        }
    else:
        context = {
            'u_form': u_form,
            'p_form': p_form,
            'orders': orders,
            'total_orders': total_orders,
            'total_spent': total_spent
        }
    
    return render(request, 'users/profile.html', context)