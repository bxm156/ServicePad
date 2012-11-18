# Create your views here.
from django.shortcuts import render

def index(request):
    show_account_link = False
    if request.user.is_authenticated():
        show_account_link = True
    context = {'user_loggedin': show_account_link}
    return render(request,'index.djhtml',context)