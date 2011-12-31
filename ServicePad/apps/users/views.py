# Create your views here.
import hashlib, random, datetime
from forms import RegistrationForm
from models import Volunteer

from django.shortcuts import render_to_response, RequestContext, redirect, get_object_or_404
from django.core.exceptions import MultipleObjectsReturned

def register(request):    
    if request.POST:
        new_data = request.POST.copy()
        registration = RegistrationForm(new_data)
        if registration.is_valid():
            #Create user
            new_user = registration.save()
            
            #Email confirmation
            salt = str(random.random())
            hash_salt = hashlib.sha224(salt).hexdigest()
            activation_key = hashlib.sha224(hash_salt + new_user.username).hexdigest()[:32]
            key_expires = datetime.datetime.today() + datetime.timedelta(days=1)
            new_profile = Volunteer(user=new_user,
                                    activation_key=activation_key,
                                    key_expires=key_expires
                        )
            new_profile.save()
            url = request.get_host() + "/register/confirm/%u/%s" % (new_user.id,activation_key)
            return render_to_response('users/register_thankyou.html',{'url':url})
        else:
            context = RequestContext(request,
                                     {'errors':registration.errors,
                                     'form':registration})
            return render_to_response('users/register.html', context)

    registration = RegistrationForm()
    context = RequestContext(request,
           {'form':registration}
    )
    return render_to_response('users/register.html', context)

def confirm(request, user, key):
    if request.user.is_authenticated():
        #Users is logged in and already confirmed
        return redirect("/account")
    #Verify the confirmation request
    try:
        user_profile = get_object_or_404(Volunteer, id=user, activation_key=key)
    except MultipleObjectsReturned:
        return render_to_response('users/confirm.html', {'success':False})
        
    if user_profile.key_expires < datetime.datetime.today():
        #Resend the confirmation email with a new confirmation challenge
        return render_to_response('users/confirm.html', {'expired':True})
    #If valid
    user_account = user_profile.user
    if user_account.is_active:
        #User was already activated
        return redirect("/")
    #Activate User
    user_account.is_active = True
    user_account.save()
    return render_to_response('users/confirm.html', {'success':True})
