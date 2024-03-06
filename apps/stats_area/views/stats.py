from django.shortcuts import render, redirect, HttpResponse

def stats(request):
    return render(request, 'stats.html')