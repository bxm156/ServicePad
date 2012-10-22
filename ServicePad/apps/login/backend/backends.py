from django_cas.backends import CASBackend
from ServicePad.apps.account.models import UserProfile
import ldap

class PopulatedCASBackend(CASBackend):
    
    def authenticate(self,ticket,service):
        
        user = super(PopulatedCASBackend, self).authenticate(ticket,service)
        if user:
            user.profile, created = UserProfile.objects.get_or_create(user=user)
            if created:
                self.populate_user(user)
                user.save()
                user.profile.save()
        return user
    
    def populate_user(self,user):
        conn = ldap.initialize('ldap://ldap.case.edu')
        conn.simple_bind_s()
        search = "uid={}".format(user.username)
        baseDNS = "ou=People,o=cwru.edu,o=isp"    
        results = conn.search_s(baseDNS, ldap.SCOPE_SUBTREE, search)
        print results
        if results and len(results) == 1:
            diction = results[0][1]
            user.first_name = diction['givenName'][0]
            user.last_name = diction['sn'][0]
            user.email = diction['mail'][0]
        