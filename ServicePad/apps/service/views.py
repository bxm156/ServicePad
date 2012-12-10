# Create your views here.

from ServicePad.apps.service.models import ServiceEnrollment, ServiceRecord
from ServicePad.apps.service.forms import ServiceReviewForm

from django.shortcuts import get_object_or_404, render, redirect

def review(request,enrollment_id):
    se = ServiceEnrollment.objects.filter(pk=enrollment_id).values('event__owner_id','event_id','event__name','user_id','user__first_name','user__last_name',
                'team_id','team__name','start','end')[0]
    if request.user.id != int(se['event__owner_id']):
        return redirect("/events/")
    record = ServiceRecord(event_id=se['event_id'],user_id=se['user_id'],team_id=se['team_id'])
    context = {'enrollment':se}
    if request.method == "POST":
        review_form = ServiceReviewForm(request.POST.copy(),instance=record)
        if review_form.is_valid():
            review_form.save()
            se = ServiceEnrollment.objects.get(pk=enrollment_id)
            se.approved = 2
            se.save()
            return redirect("/events/{}/admin/".format(se.event_id))
    else:
        review_form = ServiceReviewForm(instance=record)
    context.update({'form':review_form})
    return render(request,'service_review.djhtml',context)
    