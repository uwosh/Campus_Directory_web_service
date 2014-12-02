# $Id$

# returns the class (by class number and term code) instructor email address

import re
import xmlrpclib
Randy_Loch = '192.168.0.1'
Kim_Nguyen_G5 = '192.168.0.1'
Kim_Nguyen_Air = '192.168.0.1'
Kim_Nguyen_iMac = '192.168.0.1'
John_Hren_MBP = '192.168.0.1'
CMF2 = '192.168.0.1'
Plone1 = '192.168.0.1'
Plone3 = '192.168.0.1'

def getInstructorEmailByClassNumberTerm (self, class_nbr, strm):
    request = self.REQUEST
    RESPONSE =  request.RESPONSE
    remote_addr = request.REMOTE_ADDR
    if remote_addr in [Plone1, CMF2, Randy_Loch, Kim_Nguyen_Air, Kim_Nguyen_G5, Kim_Nguyen_iMac, John_Hren_MBP, Plone3, '127.0.0.1', ]:
        conn = getattr(self, 'Oracle_Database_Connection_NGUYEN_PRD')
        connstr = conn.connection_string
        try:
            if not conn.connected():
                conn.connect(connstr)
        except:
            conn.connect(connstr)
        dbc = conn()
        querystr = "select email_addr from ps_email_addresses where e_addr_type = 'CAMP' and emplid = (select emplid from ps_class_instr where crse_id = (select crse_id from ps_class_tbl where class_nbr = '%s' and strm = '%s') and strm = '%s' and class_section = (select class_section from ps_class_tbl where class_nbr = '%s' and strm = '%s') )" % (class_nbr, strm, strm, class_nbr, strm)

        try:
            retlist = dbc.query (querystr)
        except:
            # try the query a second time since it can fail to connect the first time
            conn.connect(connstr)
            dbc = conn()
            retlist = dbc.query (querystr)

        if len(retlist) == 2:
            if len(retlist[1]) == 1:
                if len(retlist[1][0]) == 1:
                    current_semester = retlist[1][0][0]

        if len(retlist) == 2:
            if len(retlist[1]) == 1:
                if len(retlist[1][0]) == 1:
                    return retlist[1][0][0]

        return "error: unable to determine the instructor email address"
