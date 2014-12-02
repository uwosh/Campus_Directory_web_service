# getClassesWithInstructorsByTerm - get info (including instructor) on classes offered in a semester; does not include classes without an assigned instructor

import re
import xmlrpclib
import cx_Oracle
import logging
logger = logging.getLogger("getClassesWithInstructorsByTerm")

#Randy_Loch = '192.168.0.1'
Kim_Nguyen_G5 = '192.168.0.1'
Kim_Nguyen_Air = '192.168.0.1'
Kim_Nguyen_iMac = '192.168.0.1'
John_Hren_MBP = '192.168.0.1'
#CMF2 = '192.168.0.1'
Plone1 = '192.168.0.1'
Plone3 = '192.168.0.1'
Joel_Herron_iMac = '192.168.0.1'

def getClassesWithInstructorsByTerm(self, strm):
    request = self.REQUEST
    RESPONSE =  request.RESPONSE
    remote_addr = request.REMOTE_ADDR
    if remote_addr in [Plone1, Kim_Nguyen_Air, Kim_Nguyen_G5, Kim_Nguyen_iMac, John_Hren_MBP, Plone3, Joel_Herron_iMac, '127.0.0.1', ]:
        conn = getattr(self, 'Oracle_Database_Connection_NGUYEN_PRD')
        connstr = conn.connection_string
        try:
            if not conn.connected():
                conn.connect(connstr)
        except:
            conn.connect(connstr)
        dbc = conn()
        querystr = """
select 
 c.subject,
 c.catalog_nbr,
 c.descr,
 c.class_section,
 c.crse_id,
 c.session_code,
 c.acad_group,
 c.class_nbr,
 c.strm,
 n.first_name,
 n.last_name, 
 e.email_addr,
 cc.course_title_long
from
 ps_class_tbl c,
 ps_names n,
 ps_class_instr i,
 ps_email_addresses e, 
 ps_crse_catalog cc     
where 
 c.strm = '%s'
 and c.institution = 'UWOSH' 
 and c.crse_id = i.crse_id 
 and i.strm = c.strm 
 and i.class_section = c.class_section 
 and n.emplid = i.emplid 
 and n.eff_status = 'A' 
 and n.name_type = 'PRI' 
 and n.effdt = (select max(effdt) from ps_names n2 where n2.emplid = n.emplid 
		and n2.eff_status = n.eff_status 
		and n2.name_type = n.name_type) 
 and e.emplid = i.emplid 
 and e_addr_type = 'CAMP'
 and c.crse_id = cc.crse_id 
 and cc.effdt = (select max(effdt) from ps_crse_catalog where crse_id = cc.crse_id and eff_status = 'A')
 and cc.eff_status = 'A'     
""" % strm

        try:
            retlist = dbc.query (querystr)
        except:
            # try the query a second time since it can fail to connect the first time
            conn.connect(connstr)
            dbc = conn()
            retlist = dbc.query (querystr)

        myMarshaller = xmlrpclib.Marshaller()
        return myMarshaller.dumps(retlist)
