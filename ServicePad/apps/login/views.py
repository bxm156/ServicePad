# Create your views here.
import django.contrib.auth
from django.shortcuts import render_to_response, RequestContext, redirect
from forms import LoginForm

# Currently not used
def login(request):
    loginForm = LoginForm()
    if request.POST:
        new_data = request.POST.copy()
        loginForm = LoginForm(new_data)
        if loginForm.is_valid():
            email = loginForm.cleaned_data['username']
            password = loginForm.cleaned_data['password']
            user = django.contrib.auth.authenticate(username=email, password=password)
            if user is not None:
                if user.is_active:
                    django.contrib.auth.login(request,user)
                    return redirect("/account")
                else:
                    #Account not active
                    pass
            else:
                #Invalid login info
                pass
       
    context = RequestContext(request,
                             {'form':loginForm,
                              'errors':loginForm.errors
                              })
    return render_to_response('login.html',context)