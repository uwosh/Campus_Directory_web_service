# $Id$

# returns the current (if available) and next PeopleSoft semester codes with matching descriptions, as of today

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

def getNextSemestersWithDescription(self):
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
        querystr = "select strm, descr from ps_term_tbl where institution = 'UWOSH' and acad_career = 'UGRD' and term_begin_dt <= sysdate and term_end_dt >= sysdate"

        try:
            retlist = dbc.query (querystr)
        except:
            # try the query a second time since it can fail to connect the first time
            conn.connect(connstr)
            dbc = conn()
            retlist = dbc.query (querystr)

        if len(retlist) == 2:
            if len(retlist[1]) == 1:
                if len(retlist[1][0]) == 2:
                    current_semester = retlist[1][0][0]
                    current_semester_descr = retlist[1][0][1]

        if current_semester:
            # now grab the next semester's code, knowing the current semester code
            querystr2 = "select t1.strm, t1.descr from ps_term_tbl t1 where t1.institution = 'UWOSH' and t1.acad_career = 'UGRD' and t1.strm = (select min(strm) from ps_term_tbl t2 where t2.institution = t1.institution and t2.acad_career = t1.acad_career and t2.strm > '%s')" % current_semester
        else:
            # grab the next semester code, a bit differently from above because we are not currently in a semester
            querystr2 = "select t1.strm, t1.descr from ps_term_tbl t1 where t1.institution = 'UWOSH' and t1.acad_career = 'UGRD' and t1.term_begin_dt = (select min(term_begin_dt) from ps_term_tbl t2 where t2.institution = t1.institution and t2.acad_career = t1.acad_career and term_begin_dt > sysdate)"

        try:
            retlist = dbc.query (querystr2)
        except:
            # try the query a second time since it can fail to connect the first time
            conn.connect(connstr)
            dbc = conn()
            retlist = dbc.query (querystr2)

        if len(retlist) == 2:
            if len(retlist[1]) == 1:
                if len(retlist[1][0]) == 2:
                    next_semester = retlist[1][0][0]
                    next_semester_descr = retlist[1][0][1]

        myMarshaller = xmlrpclib.Marshaller()

        if current_semester:
            # return array of both semester data
            return myMarshaller.dumps([(current_semester, current_semester_descr), (next_semester, next_semester_descr),])
            #return([(current_semester, current_semester_descr), (next_semester, next_semester_descr),])
        else:
            if next_semester:
                # return array of just next semester data
                return myMarshaller.dumps([(next_semester, next_semester_descr),])
                #return([(next_semester, next_semester_descr),])
            else:
                return "error: unable to determine the next semester code"
