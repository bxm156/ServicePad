from django import forms
from ServicePad.apps.account.models import UserProfile, Availability, HasSkill, HasInterest

class VolunteerProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        exclude = ('organization_name','organization_address','organization_city',
                   'organization_state','organization_postalzip','organization_phone',)
        
        
class OrganizationProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        exclude = ('major','graduating_class',)
        
class AvailabilityForm(forms.ModelForm):
    
    class Meta:
        model = Availability
        exclude = ('user')
        
class AddSkillForm(forms.ModelForm):
    #forms.ModelChoiceField(queryset = EventCategory.objects.all(), empty_label=None)
    class Meta:
        model = HasSkill
        exclude = ('user')
        
class AddInterestForm(forms.ModelForm):

    class Meta:
        model = HasInterest
        exclude = ('user')