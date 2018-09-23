from django.shortcuts import render, HttpResponse, redirect

app_name = 'dopenotes'
def index(request):
    return render(request, 'home.html')