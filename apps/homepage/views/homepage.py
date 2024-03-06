from django.shortcuts import render, redirect, HttpResponse

def homepage(request):
    return render(request, 'homepage.html')