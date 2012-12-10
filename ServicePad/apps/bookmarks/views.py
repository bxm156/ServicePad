# Create your views here.
from models import Bookmark
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def bookmark(request,eid):
    try:
        bookmark = Bookmark.objects.get(user=request.user,event_id=eid)
    except Bookmark.DoesNotExist:
        bookmark = Bookmark(user=request.user,event_id=eid)
        bookmark.save()
    return redirect(bookmark)

@login_required
def remove_bookmark(request,eid):
    try:
        Bookmark.objects.get(user=request.user,event_id=eid).delete()
    except:
        pass
    return redirect("/account")