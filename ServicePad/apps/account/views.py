# Create your views here.
from django.shortcuts import render_to_response, redirect, RequestContext


def index(request):
    if request.user.is_authenticated():
        return render_to_response('account_index.html',{},
                                  context_instance=RequestContext(request))
    return redirect("/")


def teams(request):
    pass

def profile(request):
    pass

def track(request):
    pass
    