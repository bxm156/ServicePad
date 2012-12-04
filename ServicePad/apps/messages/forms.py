from django import forms
from models import Message
    
class ComposeMessageForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ComposeMessageForm, self).__init__(*args, **kwargs)
        self.fields['toUser'].label = "To"
    
    class Meta:
        model = Message
        exclude = ('fromUser')