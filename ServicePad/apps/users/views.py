# Create your views here.
from forms import RegistrationForm
from django.shortcuts import render_to_response, RequestContext

def register(request):    
    if request.POST:
        print "DATA FOUND"
        new_data = request.POST.copy()
        registration = RegistrationForm(new_data)
        if registration.is_valid():
            #Create user
            print registration.cleaned_data.get('first_name')
        else:
            print registration.errors
    registration = RegistrationForm()
    context = RequestContext(request,
           {'form':registration}
    )
    return render_to_response('users/register.html',context)
        