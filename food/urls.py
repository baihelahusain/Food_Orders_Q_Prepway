from .import views
from django.urls import path

app_name = 'food'
urlpatterns = [
    path('', views.index, name='index'),
    #/food/1
    path("<int:item_id>/", views.detail,name='detail'),
    #add item
    path('add/', views.create_item,name='create_item'),
    path('item/', views.item, name='item'),
    #edit
    path('update<int:id>/',views.update_item,name='update_item'),
    #delete
    path('delete<int:id>/',views.delete_item,name='delete_item'),
    
    # Cart URLs
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('order-history/', views.order_history, name='order_history'),
    
    # Superuser order management URLs
    path('all-orders/', views.all_orders, name='all_orders'),
    path('order-detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('delete-order/<int:order_id>/', views.delete_order, name='delete_order'),
]
