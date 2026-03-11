from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse

from .cart import Cart
from .models import OrderList, PasswordReset, Checkout, Product, Category,Profile

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

def cart(request):
    return render(request, "cart.html")


def account(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'delete_account':
            user = request.user
            logout(request)
            user.delete()
            messages.success(request, "Your account has been deleted.")
            return redirect('register')

        return redirect('account')

    return render(request, 'account.html', {'profile': profile})

def order_list(request):
    orders = OrderList.objects.all()
    return render(request, 'order_list.html', {'orders': orders})


# Edit order
def order_edit(request, id):
    order = get_object_or_404(OrderList, id=id)

    if request.method == "POST":
        order.customer_name = request.POST.get('customer_name')
        order.status = request.POST.get('status')
        order.total_amount = request.POST.get('total_amount')
        order.save()
        return redirect('order_list')

    return render(request, 'edit_order.html', {'order': order})


# Delete order
def order_delete(request, id):
    order = get_object_or_404(OrderList, id=id)

    if request.method == "POST":
        order.delete()
        return redirect('order_list')

    return redirect('order_list')

def checkout(request):

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


def checkout_success(request):
    return render(request, 'checkout_success.html')

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


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    images = product.images.all()

    context = {
        'product': product,
        'images': images,
    }
    return render(request, 'product_detail.html', context)

# Cart views

def cart_detail(request):
    cart = Cart(request)
    context = {'cart': cart}
    return render(request, 'cart.html', context)


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    quantity = int(request.POST.get('quantity', 1))
    override = request.POST.get('override_quantity', False) == 'True'

    cart.add(product=product, quantity=quantity, override_quantity=override)
    return redirect('cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

@login_required(login_url='/login/')
def notifications(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile.notifications = 'notifications' in request.POST
        profile.save()
        messages.success(request, 'Notification preferences saved.')
        return redirect('notifications')
    return render(request, 'notifications.html', {'profile': profile})

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
