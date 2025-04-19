"""
URL configuration for foodsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.urls import include
from users import views as user_views
from django.contrib.auth import views as authentication_views
from django.contrib.auth.views import LogoutView  
from django.conf import settings
from django.conf.urls.static import static
from users.forms import UserLoginForm
from django.views.generic.base import RedirectView


urlpatterns = [
    path("", RedirectView.as_view(pattern_name='food:index'), name='home'),
    path("admin/", admin.site.urls),
    path("food/", include("food.urls")),
    path('register/', user_views.register, name='register'),
    path('login/', authentication_views.LoginView.as_view(
        template_name='users/login.html',
        authentication_form=UserLoginForm
    ), name='login'),
    path('logout/', LogoutView.as_view(
        template_name='users/logout.html',
        next_page='food:index'  # Redirect after logout
    ), name='logout'),
    path('profile/', user_views.profilepage, name='profile'),
]

# Add static and media URL patterns correctly
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)