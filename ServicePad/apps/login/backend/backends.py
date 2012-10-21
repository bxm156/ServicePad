from django_cas.backends import CASBackend

class PopulatedCASBackend(CASBackend):
    
    def authenticate(self,ticket,service):
        
        user = super(PopulatedCASBackend, self).authenticate(ticket,service)
        
        #Modify user
        
        return user