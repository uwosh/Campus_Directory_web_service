import re
try:
    import json
except ImportError:
    import simplejson as json
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
John_Hren_MBP = '192.168.0.1'

def getClassInfoByTermAndSubjectAndCatalogNumberAndSectionJSONPCX(self, strm, subject, catalog_nbr, section, callback="?"):
    request = self.REQUEST
    RESPONSE =  request.RESPONSE
    remote_addr = request.REMOTE_ADDR
    if remote_addr in [Kim_Nguyen_iMac, '127.0.0.1', Plone3, ws_it_uwosh_edu, Kim_Nguyen_MacBook, Kim_Nguyen_MacBook_IDEA_Lab, Kim_Nguyen_G5, John_Hren_MBP]:
        file = open('/opt/Plone-2.5.5/zeocluster/client2/Extensions/Oracle_Database_Connection_NGUYEN_PRD.txt', 'r')
        for line in file.readlines():
            if line <> "" and not line.startswith('#'):
                connString = line
        file.close()
        connection = cx_Oracle.connect(connString)
        cursor = connection.cursor()
        cursor.execute("""
select 
 c.class_nbr,
 c.session_code,
 n.first_name,
 n.last_name, 
 e.email_addr
from
 ps_class_tbl c,
 ps_names n,
 ps_class_instr i,
 ps_email_addresses e
where 
 c.strm = :arg1
 and c.institution = 'UWOSH' 
 and c.subject = :arg2
 and c.catalog_nbr = :arg3
 and c.class_section = :arg4
 and i.crse_id = c.crse_id
 and i.crse_offer_nbr = c.crse_offer_nbr
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
""",
                       arg1 = strm, arg2 = subject, arg3 = catalog_nbr, arg4 = section)
        retlist = []
        for column_1 in cursor:
            retlist.append([column_1, ])
        data = json.dumps(retlist)
        return callback + "(" + data + ");"
