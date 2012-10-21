from django_cas.blackends import CASBackend

class PopulatedCASBackend(CASBackend):
    
    def authenticate(self,ticket,service):
        
        user = super(PopulatedCASBackend, self).authenticate(ticket,service)
        
        #Modify user
        
        return user