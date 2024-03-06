from django.shortcuts import render, redirect, HttpResponse

def exercise(request):
    return render(request, 'exercise.html')