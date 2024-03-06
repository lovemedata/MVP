from django.shortcuts import render, redirect, HttpResponse

def note(request):
    return render(request, 'note.html')