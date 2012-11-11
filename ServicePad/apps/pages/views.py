# Create your views here.
from django.shortcuts import render_to_response, RequestContext

def index(request):
    return render_to_response('index.djhtml',
                              {},
                              context_instance=RequestContext(request))