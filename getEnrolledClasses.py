# $Id$

# returns the classes the student is enrolled in

import re
import xmlrpclib
#import logging
#logger = logging.getLogger("getEnrolledClasses")
#from common import *
ResLife_MIO_1 = '192.168.0.1'
ResLife_MIO_2 = '192.168.0.1'
ResLife_MIO_3 = '192.168.0.1'
Kim_Nguyen_G5 = '192.168.0.1'
Kim_Nguyen_Air = '192.168.0.1'
#John_Dorapalli = '192.168.0.1'
Marshall_Scorcio_1 = '192.168.0.1'
Marshall_Scorcio_2 = '192.168.0.1'
Greg_Duescher_MIO = '192.168.0.1'
Joel_Kleier_MIO = '192.168.0.1'
CMF2 = '192.168.0.1'
Randy_Loch = '192.168.0.1'
Plone1 = '192.168.0.1'
Plone3 = '192.168.0.1'

def getEnrolledClasses (self, emplid, strm):
    request = self.REQUEST
    RESPONSE =  request.RESPONSE
    remote_addr = request.REMOTE_ADDR
    if remote_addr in [Randy_Loch, Kim_Nguyen_G5, Kim_Nguyen_Air, '192.168.0.1', '127.0.0.1', CMF2, Plone1, Plone3 ]:
        conn = getattr(self, 'Oracle_Database_Connection_NGUYEN_PRD')
        connstr = conn.connection_string
        try:
            if not conn.connected():
                conn.connect(connstr)
        except:
            conn.connect(connstr)
        dbc = conn()
        querystr = "select c.subject, c.catalog_nbr, c.descr, c.class_section, c.crse_id, n.first_name, n.last_name, e.email_addr, i.emplid from ps_email_addresses e, ps_class_tbl c, ps_class_instr i, ps_names n where c.class_nbr in (select class_nbr from PS_STDNT_ENRL_VW where emplid = '%s' and strm = c.strm and institution = c.institution) and c.strm = '%s' and c.institution = 'UWOSH' and c.crse_id = i.crse_id and i.strm = c.strm and i.class_section = c.class_section and n.emplid = i.emplid and n.eff_status = 'A' and n.name_type = 'PRI' and n.effdt = (select max(effdt) from ps_names n2 where n2.emplid = n.emplid and n2.eff_status = n.eff_status and n2.name_type = n.name_type) and e.emplid = i.emplid and e_addr_type = 'CAMP'" % (emplid, strm)
        try:
            retlist = dbc.query (querystr)
        except:
            conn.connect(connstr)
            dbc = conn()
            retlist = dbc.query (querystr)
        # if len(retlist) == 2:
#             if len(retlist[1]) == 1:
#                 if len(retlist[1][0]) == 1:
#                     return retlist[1][0][0]
#         return "error: no semester code found matching today's date"
        #logger.info("Got retlist '%s'" % retlist)
        myMarshaller = xmlrpclib.Marshaller()
        return myMarshaller.dumps(retlist)
