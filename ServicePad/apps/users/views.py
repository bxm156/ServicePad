# Create your views here.
import hashlib, random, datetime
from forms import RegistrationForm
from models import Volunteer

from django.shortcuts import render_to_response, RequestContext

def register(request):    
    if request.POST:
        new_data = request.POST.copy()
        registration = RegistrationForm(new_data)
        if registration.is_valid():
            #Create user
            new_user = registration.save();
            
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
        else:
            context = RequestContext(request,
                                     {'errors':registration.errors,
                                     'form':registration})
            return render_to_response('users/register.html',context)

    registration = RegistrationForm()
    context = RequestContext(request,
           {'form':registration}
    )
    return render_to_response('users/register.html', context)