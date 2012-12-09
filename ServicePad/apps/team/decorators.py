from django.shortcuts import redirect
from ServicePad.apps.team.models import Team

def team_admin_required(function=None,redirect_to="/account/"):
    """
    Decorator that only allows a team admin. The original view must have
    an argument "team_id" which is the id of a team to check the administer of.
    If the user is the administer of that team, the view is shown. Otherwise,
    the user is redirected to the "redirect_to" value (Default: /account/)
    """
    def _decorated(view_func):
        def _view(request, *args, **kwargs):
            if 'team_id' in kwargs:
                team = Team.objects.get(pk=kwargs['team_id'])
                if team.admin == request.user:
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