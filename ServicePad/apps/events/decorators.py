from django.shortcuts import redirect
from ServicePad.apps.events.models import Event
import sys
def event_admin(function=None,redirect_to="/events/"):
    """
    Decorator that only allows an event admin. The original view must have
    an argument "event_id" which is the id of a event to check the administer of.
    If the user is the administer of that event, the view is shown. Otherwise,
    the user is redirected to the "redirect_to" value (Default: /events)
    """
    def _decorated(view_func):
        def _view(request, *args, **kwargs):
            if 'event_id' in kwargs:
                event_id = int(kwargs['event_id'])
                owner_id = Event.objects.filter(pk=event_id).values('owner_id')[:1]
                owner_id = owner_id[0]['owner_id']
                if request.user.id == owner_id:
                    return view_func(request,*args,**kwargs)
            return redirect(redirect_to)
        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__
        return _view
    if function is None:
        return _decorated
    else:
        return _decorated(function)