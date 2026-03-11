"""
URL configuration for myapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from eduka import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('register/', views.registerview, name='register'),
    path('login/', views.loginview, name='login'),
    path('base/',views.base,name='base'),
    path('cart/', views.cart, name='cart'),
    path('', views.index, name='index'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('logout/',views.logoutview, name='logout'),
    path('password_reset_sent/<str:reset_id>/', views.password_reset_sent, name='password_reset_sent'),
    path('reset_password/<str:reset_id>/', views.reset_password, name='reset_password'),
    path('checkout/', views.lipa_na_mpesa, name='checkout')

]
