# Create your views here.
from django.shortcuts import render_to_response, redirect
from django import template

def index(request):
    if request.user.is_authenticated():
        return render_to_response('index.html')
    return redirect("/")


def teams(request):
    pass

def profile(request):
    pass

def track(request):
    pass
    