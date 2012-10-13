# Create your views here.
import datetime
from forms import UserRegistrationForm, OrganizationRegistrationForm
from ServicePad.apps.account.models import UserProfile
from django.shortcuts import render_to_response, RequestContext, redirect, get_object_or_404
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth.models import User
from ServicePad.exceptions import InvalidRegistrationRequest
from ServicePad.emailer import send_email

def register(request,**kwargs):    
    if request.POST:
        new_data = request.POST.copy()
        #Create form with user data
        
        account_type = int(new_data['form_type'])
        if account_type is UserProfile.ACCOUNT_VOLUNTEER:
            registration = UserRegistrationForm(new_data)
        elif account_type is UserProfile.ACCOUNT_ORGANIZATION:
            registration = OrganizationRegistrationForm(new_data)
        else:
            raise InvalidRegistrationRequest
        
        #Process data
        if registration.is_valid():
            #Create user
            new_user = registration.save()
            
            #Email confirmation
            #salt = str(random.random())
            #hash_salt = hashlib.sha224(salt).hexdigest()
            #activation_key = hashlib.sha224(hash_salt + new_user.username).hexdigest()[:32]
            #key_expires = datetime.datetime.today() + datetime.timedelta(days=1)
            #new_profile = UserProfile(user=new_user,
            #                        activation_key=activation_key,
            #                        key_expires=key_expires,
            #                        account_type=account_type
            #            )
            
            #new_profile.save()
            url = request.get_host() + "/register/confirm/%u/%s" % (new_user.id,new_user.get_profile().activation_key)
            send_email(new_user.username,"Activation Email",url)
            return render_to_response('register_thankyou.html',{'url':url})
        else:
            context = RequestContext(request,
                                     {'errors':registration.errors,
                                     'form':registration})
            return render_to_response('register.html', context)
    
    #Show new form
    if kwargs['type'] == UserProfile.ACCOUNT_VOLUNTEER:
        registration = UserRegistrationForm()
    elif kwargs['type'] == UserProfile.ACCOUNT_ORGANIZATION:
        registration = OrganizationRegistrationForm()
    else:
        registration = UserRegistrationForm()
    context = RequestContext(request,
           {'form':registration}
    )
    return render_to_response('register.html', context)

def confirm(request, user, key):
    if request.user.is_authenticated():
        #Users is logged in and already confirmed
        return redirect("/account")
    #Verify the confirmation request
    try:
        user = get_object_or_404(User, id=user)
    except MultipleObjectsReturned:
        return render_to_response('confirm.html', {'success':False})
    
    user_profile = user.get_profile()
    
    if user_profile.authentication != key:
        render_to_response('confirm.html', {'success':False})
    
    if user_profile.key_expires < datetime.datetime.today():
        #Resend the confirmation email with a new confirmation challenge
        return render_to_response('confirm.html', {'expired':True})
    #If valid
    user_account = user_profile.user
    if user_account.is_active:
        #User was already activated
        return redirect("/")
    #Activate User
    user_account.is_active = True
    user_account.save()
    return render_to_response('confirm.html', {'success':True})
