# $Id$

# wrapper that will try to swallow Oracle connection errors

def getEnrolledClassesWrapper (self, emplid, strm):
    try:
        return self.getEnrolledClasses(emplid, strm)
    except:
        return self.getEnrolledClasses(emplid, strm)
