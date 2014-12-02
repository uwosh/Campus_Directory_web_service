# $Id$

# wrapper that will try to swallow Oracle connection errors
import logging
logger = logging.getLogger("getClassByClassNumber")

def getClassByClassNumber (self, class_nbr, strm):
    try:
        retval = self.getClassByClassNumberInternal(class_nbr, strm)
        logger.info("First try: Got retval")
        return retval
    except Exception, e:
        retval= self.getClassByClassNumberInternal(class_nbr, strm)
        logger.info("Second try: Got retval, exception was %s" % e)
        return retval
    else:
        logger.info("No exception occurred")
