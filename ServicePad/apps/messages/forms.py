from django import forms
from models import Message
    
class ComposeMessageForm(forms.ModelForm):
    
    class Meta:
        model = Message
        exclude = ('fromUser')