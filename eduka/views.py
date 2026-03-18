from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django_daraja.mpesa.core import MpesaClient
from .models import Order, OrderItem, Profile

from .cart import Cart
from .models import OrderList, PasswordReset, Checkout, Product, Category

# Create your views here.

def index(request):
    featured_products = Product.objects.filter(available=True)[:8]
    categories = Category.objects.all()
    total_products = Product.objects.filter(available=True).count()
    total_categories = Category.objects.count()

    context = {
        'featured_products': featured_products,
        'categories': categories,
        'total_products': total_products,
        'total_categories': total_categories,
    }
    return render(request, 'index.html', context)

def base(request):
    return render(request, 'base.html')

def loginview(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect("product_list")
        else:
            messages.error(request, "Invalid Login credentials")
            return redirect("login")
    return render(request, "login.html")

def registerview(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")


        user_data_has_error = False

        if User.objects.filter(username=username).exists():
            user_data_has_error = True
            messages.error(request, "Username already exists")

        if User.objects.filter(email=email).exists():
            user_data_has_error = True
            messages.error(request, "Email already exists")
        if len(password) < 8:
            user_data_has_error = True
            messages.error(request, "Password must be at least 8 characters long")

        if user_data_has_error:
            return redirect('register')
        else:
            new_user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password

            )
            messages.success(request, "User created successfully")
            return redirect('login')

    return render(request, "register.html")

def logoutview(request):
    logout(request)
    return redirect('login')

def forgot_password(request):
    if request.method=="POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)
            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()

            password_reset_url = reverse("reset_password" , kwargs ={"reset_id": new_password_reset.reset_id})
            full_password_reset_url = f"{request.scheme}://{request.get_host()}{password_reset_url}"
            email_body = f"Reset your password  using the link below:\n\n\n{full_password_reset_url}"

            email_message = EmailMessage(
                "Reset your password",
                email_body,
                settings.EMAIL_HOST_USER,
                [email]
            )
            email_message.fail_silently = True
            email_message.send()

            return redirect('password_reset_sent' , reset_id = new_password_reset.reset_id)

        except User.DoesNotExist:
            messages.error(request, f"No user with email {email} found")
            return redirect('forgot_password')
    return render(request, "forgot_password.html")

def password_reset_sent(request , reset_id):
    if PasswordReset.objects.filter(reset_id = reset_id).exists():
        return render( request, 'password_reset_sent.html')
    else:
        messages.error(request, "Invalid reset id")
        return redirect('forgot_password')


def reset_password(request , reset_id):


        try:
            password_reset_id = PasswordReset.objects.get(reset_id=reset_id)

            if request.method == "POST":
                password = request.POST.get("password", "")
                confirm_password = request.POST.get("confirm_password")

                password_have_error = False

                if password != confirm_password:
                    password_have_error = True
                    messages.error(request, "Password do not match")

                if not password or  len(password) < 8:
                    password_have_error = True
                    messages.error(request, 'Password must be at least 8 characters long')

                expiration_time = password_reset_id.created_when + timezone.timedelta(minutes=10)

                if timezone.now() > expiration_time:
                    password_reset_id.delete()
                    messages.error(request, 'Reset link has expired')
                    return redirect('forgot_password')



                if not password_have_error:
                    user = password_reset_id.user
                    user.set_password(password)
                    user.save()

                    password_reset_id.delete()

                    messages.success(request, 'Password reset. Proceed to login')
                    return redirect('login')

                else:
                    return render(request, 'reset_password.html')




        except PasswordReset.DoesNotExist:


            messages.error(request, 'Invalid reset link')
            return redirect('forgot_password')


        return render(request, "reset_password.html")



def order_list(request):
    return render(request, 'order_list.html')

def order_edit(request, id):
    pass

def order_delete(request, id):
    pass

    if request.method == "POST":

        Checkout.objects.create(
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            product_name=request.POST.get('product_name'),
            quantity=request.POST.get('quantity'),
            total_price=request.POST.get('total_price'),
            payment_method=request.POST.get('payment_method')
        )

        return redirect('checkout_success')

    return render(request, 'checkout.html')

def checkout_details(request):
    if request.method == "POST":

        Checkout.objects.create(
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            product_name=request.POST.get('product_name'),
            quantity=request.POST.get('quantity'),
            total_price=request.POST.get('total_price'),
            payment_method=request.POST.get('payment_method')
        )

        return redirect('checkout_success')

    return render(request, 'checkout_details.html')

def checkout_success(request):
    return render(request, 'checkout_success.html')

# Lipa na M-pesa views
def lipa_na_mpesa(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('product_list')
    context = {
        'cart': cart,
        'total': cart.get_total(),
    }
    return render(request, 'checkout.html', context)

@login_required
def initiate_payment(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        cart  = Cart(request)
        total = cart.get_total()

        # Validate phone
        if not phone or len(phone) < 10:
            messages.error(request, 'Please enter a valid phone number e.g. 0712345678')
            return redirect('checkout')

        # Create order
        order = Order.objects.create(
            user         = request.user if request.user.is_authenticated else None,
            total_amount = total,
            phone_number = phone,
            status       = 'pending',
        )

        # Save order items
        for item in cart:
            OrderItem.objects.create(
                order    = order,
                product  = item['product'],
                quantity = item['quantity'],
                price    = item['price'],
            )

        # Send STK push
        try:
            cl = MpesaClient()
            response = cl.stk_push(
                phone,
                int(total),
                f'Order-{order.id}',
                f'EduKa Stationery Order {order.id}',
                settings.MPESA_CALLBACK_URL
            )

            if response.checkout_request_id:
                order.checkout_request_id = response.checkout_request_id
                order.save()
                messages.success(request, f'Mpesa prompt sent to {phone}. Enter your PIN to complete payment.')
                return redirect('order_pending', order_id=order.id)
            else:
                order.status = 'failed'
                order.save()
                messages.error(request, f'Failed to send prompt: {response.error_message}')
                return redirect('checkout')

        except Exception as e:
            order.status = 'failed'
            order.save()
            messages.error(request, f'Error: {str(e)}')
            return redirect('checkout')

    return redirect('checkout')

def order_pending(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Refresh page every 5 seconds to check payment status
    if order.status == 'paid':
        return redirect('payment_success', order_id=order.id)

    if order.status == 'failed':
        messages.error(request, 'Payment failed. Please try again.')
        return redirect('checkout')

    context = {'order': order}
    return render(request, 'order_pending.html', context)
@csrf_exempt
def mpesa_callback(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            result              = data['Body']['stkCallback']
            checkout_request_id = result['CheckoutRequestID']
            result_code         = result['ResultCode']

            order = Order.objects.get(checkout_request_id=checkout_request_id)

            if result_code == 0:
                items            = result['CallbackMetadata']['Item']
                mpesa_code       = next(i['Value'] for i in items if i['Name'] == 'MpesaReceiptNumber')
                order.status     = 'paid'
                order.mpesa_code = mpesa_code
                order.save()
                # Clear the cart
                if 'cart' in request.session:
                    del request.session['cart']
            else:
                order.status = 'failed'
                order.save()

        except Exception as e:
            print(f"Callback error: {e}")

    return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Success'})


def check_payment_status(request, order_id):
    order = Order.objects.get(id=order_id)
    return JsonResponse({'status': order.status})


def payment_success(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'payment_success.html', {'order': order})

# Products views
@login_required
def product_list(request):
    categories = Category.objects.all()
    category_slug = request.GET.get('category')
    selected_category = None

    products = Product.objects.filter(available=True)

    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'product_list.html', context)

@login_required
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    images = product.images.all()

    context = {
        'product': product,
        'images': images,
    }
    return render(request, 'product_detail.html', context)

# Cart views
@login_required
def cart_detail(request):
    cart = Cart(request)
    context = {'cart': cart}
    return render(request, 'cart.html', context)

@login_required
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    quantity = int(request.POST.get('quantity', 1))
    override = request.POST.get('override_quantity', False) == 'True'

    cart.add(product=product, quantity=quantity, override_quantity=override)
    return redirect('cart_detail')

@login_required
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')


@login_required(login_url='/login/')
def account(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')
        # handle actions here, e.g.:
        if action == 'update':
            # process form data
            pass
        return redirect('account')

    return render(request, 'account.html', {'profile': profile})


@login_required(login_url='/login/')
def security(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'toggle_2fa':
            profile.two_factor = 'two_factor' in request.POST
            profile.save()
            status = "enabled" if profile.two_factor else "disabled"
            messages.success(request, f"Two-factor authentication {status}.")

        elif action == 'toggle_notifications':
            profile.notifications = 'notifications' in request.POST
            profile.save()
            status = "enabled" if profile.notifications else "disabled"
            messages.success(request, f"Email notifications {status}.")

        return redirect('security')

    return render(request, 'security.html', {'profile': profile})

@login_required(login_url='/login/')
def notifications(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile.notifications = 'notifications' in request.POST
        profile.order_updates = 'order_updates' in request.POST
        profile.promotions = 'promotions' in request.POST
        profile.restocks = 'restocks' in request.POST
        profile.newsletter = 'newsletter' in request.POST
        profile.save()
        messages.success(request, 'Notification preferences saved.')
        return redirect('notifications')

    return render(request, 'notifications.html', {'profile': profile})


@login_required(login_url='/login/')
def history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    total_spent = sum(o.total_amount for o in orders)
    paid_count = orders.filter(status='paid').count()
    pending_count = orders.filter(status='pending').count()

    return render(request, 'history.html', {
        'orders': orders,
        'total_spent': total_spent,
        'paid_count': paid_count,
        'pending_count': pending_count,
    })