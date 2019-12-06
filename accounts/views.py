from django.shortcuts import render, redirect

# Create your views here.

def signin(request):
    if request.method == "GET":
        return render(request,'login.html')

def sign_up(request):
    if request.method == "GET":
        return render(request,'register.html')

def sign_out(request):
    return render(request,'login.html')