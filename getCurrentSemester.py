# $Id$

# returns the current PeopleSoft semester code, as of today

import re
import xmlrpclib
Randy_Loch = '192.168.0.1'
Kim_Nguyen_G5 = '192.168.0.1'
Kim_Nguyen_Air = '192.168.0.1'
#John_Dorapalli = '192.168.0.1'
CMF2 = '192.168.0.1'
Plone1 = '192.168.0.1'
Plone3 = '192.168.0.1'

def getCurrentSemester (self):
    request = self.REQUEST
    RESPONSE =  request.RESPONSE
    remote_addr = request.REMOTE_ADDR
    if remote_addr in [Plone1, CMF2, Randy_Loch, Kim_Nguyen_Air, Kim_Nguyen_G5, Plone3, '127.0.0.1', ]:
        conn = getattr(self, 'Oracle_Database_Connection_NGUYEN_PRD')
        connstr = conn.connection_string
        try:
            if not conn.connected():
                conn.connect(connstr)
        except:
            conn.connect(connstr)
        dbc = conn()
        querystr = "select strm from ps_term_tbl where institution = 'UWOSH' and acad_career = 'UGRD' and term_begin_dt <= sysdate and term_end_dt >= sysdate"
        try:
            retlist = dbc.query (querystr)
        except:
            conn.connect(connstr)
            dbc = conn()
            retlist = dbc.query (querystr)
        if len(retlist) == 2:
            if len(retlist[1]) == 1:
                if len(retlist[1][0]) == 1:
                    return retlist[1][0][0]
        return "error: no semester code found matching current date"
        #myMarshaller = xmlrpclib.Marshaller()
        #return myMarshaller.dumps(retlist[1])
