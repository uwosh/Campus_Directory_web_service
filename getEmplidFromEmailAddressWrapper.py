# $Id$

# wrapper for getEmplidFromEmailAddress that will try to swallow Oracle connection errors

def getEmplidFromEmailAddressWrapper (self, email):
    try:
        return self.getEmplidFromEmailAddress(email)
    except:
        return self.getEmplidFromEmailAddress(email)
