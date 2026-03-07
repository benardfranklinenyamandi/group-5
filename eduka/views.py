from django.shortcuts import render

# Create your views here.
def base(request):
    return render(request, 'base.html')
def login(request):
    return render(request, "login.html")
def register(request):
    return render(request, "register.html")
def cart(request):
    return render(request, "cart.html")
def index(request):
    return render(request, "index.html")
