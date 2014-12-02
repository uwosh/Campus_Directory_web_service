# getClassesWithInstructorsByTermCX - get info (including instructor) on classes offered in a semester; does not include classes without an assigned instructor

import re
import xmlrpclib
import cx_Oracle

Kim_Nguyen_G5 = '192.168.0.1'
Kim_Nguyen_iMac = '192.168.0.1'
Kim_Nguyen_MacBook = '192.168.0.1'
Kim_Nguyen_MacBook_IDEA_Lab = '192.168.0.1'
Plone1 = '192.168.0.1'
Plone3 = '192.168.0.1'
Joel_Herron_iMac = '192.168.0.1'
ws_it_uwosh_edu = '192.168.0.1'
Maccabee_Levine = '192.168.0.1'
MIO_Helios_Server = '192.168.0.1'
David_Hietpas = '192.168.0.1'

def getClassesWithInstructorsByTermCX(self, strm):
    request = self.REQUEST
    RESPONSE =  request.RESPONSE
    remote_addr = request.REMOTE_ADDR
    if remote_addr in [Kim_Nguyen_iMac, Joel_Herron_iMac, '127.0.0.1', Plone3, ws_it_uwosh_edu, Maccabee_Levine, David_Hietpas, MIO_Helios_Server, Kim_Nguyen_MacBook, Kim_Nguyen_MacBook_IDEA_Lab]:
        file = open('/opt/Plone-2.5.5/zeocluster/client2/Extensions/Oracle_Database_Connection_NGUYEN_PRD.txt', 'r')
        for line in file.readlines():
            if line <> "" and not line.startswith('#'):
                connString = line
        file.close()
        connection = cx_Oracle.connect(connString)
        cursor = connection.cursor()
        cursor.execute("""
select 
 c.subject,
 c.catalog_nbr,
 c.descr,
 c.class_section,
 c.crse_id,
 c.session_code,
 c.acad_group,
 c.class_nbr,
 n.first_name,
 n.last_name, 
 e.email_addr,
 cc.course_title_long,
 nvl(t.descr, ''),
 im.instruction_mode, 
 im.descr
from
 ps_class_tbl c left join ps_crse_topics t on c.crse_id = t.crse_id and c.crs_topic_id = t.crs_topic_id,
 ps_names n,
 ps_class_instr i,
 ps_email_addresses e,
 ps_crse_catalog cc,
 ps_instruct_mode im
where 
 c.strm = :arg1
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
 and c.institution = im.institution
 and c.instruction_mode = im.instruction_mode
 and im.eff_status = 'A'
 and im.effdt = (select max(im2.effdt) from ps_instruct_mode im2 where im2.instruction_mode = im.instruction_mode and eff_status = 'A')
-- AND c.subject = 'ART'
--order by c.subject, c.catalog_nbr, c.class_section
""",
                       arg1 = strm)
        retlist = []
        for column_1, column_2, column_3, column_4, column_5, column_6, column_7, column_8, column_9, column_10, column_11, column_12, column_13, column_14, column_15 in cursor:
            retlist.append([column_1, column_2, column_3, column_4, column_5, column_6, column_7, column_8, column_9, column_10, column_11, column_12, column_13, column_14, column_15, ])
        myMarshaller = xmlrpclib.Marshaller(allow_none=True)
        return myMarshaller.dumps(retlist)
