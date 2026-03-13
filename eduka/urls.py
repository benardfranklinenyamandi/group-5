
from django.contrib import admin
from django.urls import path
from eduka import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('register/', views.registerview, name='register'),
    path('login/', views.loginview, name='login'),
    path('base/',views.base,name='base'),
    path('', views.index, name='index'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('logout/',views.logoutview, name='logout'),
    path('password_reset_sent/<str:reset_id>/', views.password_reset_sent, name='password_reset_sent'),
    path('reset_password/<str:reset_id>/', views.reset_password, name='reset_password'),


    path('account/', views.account, name='account'),
    path('orders/', views.order_list, name='order_list'),
    path('edit/<int:id>/', views.order_edit, name='order_edit'),
    path('delete/<int:id>/', views.order_delete, name='order_delete'),

    path('checkout/', views.lipa_na_mpesa, name='checkout'),
    path('checkout_details/', views.checkout_details, name='checkout_details'),
    path('success/', views.checkout_success, name='checkout_success'),

    path('products/', views.product_list, name='product_list'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),

    # mpesa
    path('initiate-payment/', views.initiate_payment, name='initiate_payment'),
    path('mpesa/callback/', views.mpesa_callback, name='mpesa_callback'),
    path('payment-success/<int:order_id>/', views.payment_success, name='payment_success'),
    path('payment-status/<int:order_id>/', views.check_payment_status, name='check_payment_status'),
    path('initiate-payment/', views.initiate_payment, name='initiate_payment'),
    path('order-pending/<int:order_id>/', views.order_pending, name='order_pending'),

]

