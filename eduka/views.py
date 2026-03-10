from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from .models import *

# Create your views here.
@login_required
def index(request):
    return render(request, "index.html")

def base(request):
    return render(request, 'base.html')
def loginview(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect("index")
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
    return render(request, "account.html")
