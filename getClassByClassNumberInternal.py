# $Id$

# returns info about a class given a class_nbr

import re
import xmlrpclib
import logging
logger = logging.getLogger("getClassByClassNumberInternal")
from datetime import datetime
www1_webcluster_uwosh_edu = '192.168.0.1'
Kim_Nguyen_G5 = '192.168.0.1'

def getClassByClassNumberInternal (self, class_nbr, strm):
    request = self.REQUEST
    RESPONSE =  request.RESPONSE
    remote_addr = request.REMOTE_ADDR
    debugstr = "%s/%s" % (class_nbr, strm)
    if remote_addr in [www1_webcluster_uwosh_edu, Kim_Nguyen_G5, '127.0.0.1', ]:
        connId = 'Oracle_Database_Connection_ZCC041WEBSVCUSER'
        conn = getattr(self, connId)
        logger.info("1. got conn %s ok (%s)" % (connId, debugstr))
        connstr = conn.connection_string
        logger.info("2. got connection_string ok (%s)" % debugstr)
        try:
            if not conn.connected():
                logger.info("3. not connected (%s)" % debugstr)
                conn.connect(connstr)
                logger.info("4. connected ok (%s)" % debugstr)
        except Exception, e:
            estr = str(e)
            estr = re.sub(r'Invalid connection string: </strong><CODE>(.+)</CODE>', 'Invalid connection string: </strong><CODE>[omitted]</CODE>', estr)
            logger.info("5. exception %s when checking if connected (%s)" % (estr, debugstr))
            if estr.find('Invalid connection string'):
                logger.info("5.5 exiting, unable to connect to Oracle; may not be available (%s)" % debugstr)
                myMarshaller = xmlrpclib.Marshaller()
                return myMarshaller.dumps(['unable to connect to Oracle; may not be available'])
            conn.connect(connstr)
            logger.info("6. connected ok after exception (%s)" % debugstr)
        dbc = conn()
        logger.info("7. got dbc ok (%s)" % debugstr)
        # good examples are class_nbr = '90143' and strm = '0630'
        querystr = """
                   select * from PS_ZCC041WEBSVCVW where class_nbr = '%s' and strm = '%s'
                   """ % (class_nbr, strm)
        try:
            logger.info("7.5. About to call query() with class_nbr = %s and strm = %s" % (class_nbr, strm))
            before = datetime.now()
            retlist = dbc.query (querystr)
            logger.info("8. got query results ok, elapsed time was %s (%s)" % (datetime.now()-before, debugstr))
            logger.info("8.5. result set length is %s (%s)" % (len(retlist[1]), debugstr))
        except Exception, e:
            logger.info("9. exception %s when trying to query, elapsed time was %s (%s)" % (e, datetime.now()-before, debugstr))
            conn.connect(connstr)
            logger.info("10. connected ok (%s)" % debugstr)
            dbc = conn()
            logger.info("11. got dbc ok (%s)" % debugstr)
            before2 = datetime.now()
            retlist = dbc.query (querystr)
            logger.info("12. got query results ok, elapsed time was %s (%s)" % (datetime.now()-before2, debugstr))
            logger.info("12.5. result set length is %s (%s)" % (len(retlist[1]), debugstr))
        myMarshaller = xmlrpclib.Marshaller()
        return myMarshaller.dumps(retlist)
