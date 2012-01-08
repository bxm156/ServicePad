import datetime
from haystack.indexes import *
from haystack import site
from models import Event

class EventIndex(SearchIndex):
    event_name = CharField(model_attr='event_name')
    text = CharField(document=True)
    
    def index_queryset(self):
        """"Used when the entire index for model is updated."""
        return Event.objects.all()
    
    def get_model(self):
        return Event
        
site.register(Event, EventIndex)