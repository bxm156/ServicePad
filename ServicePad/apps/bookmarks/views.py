# Create your views here.
from models import Bookmark
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def bookmark(request,id):
    try:
        bookmark = Bookmark.objects.get(user=request.user,event_id=id)
    except Bookmark.DoesNotExist:
        bookmark = Bookmark(user=request.user,event_id=id)
        bookmark.save()
    return redirect(bookmark)