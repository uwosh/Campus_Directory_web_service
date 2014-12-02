# returns the classes the student is enrolled in

import re
import xmlrpclib
#import logging
#logger = logging.getLogger("getEnrolledClasses")
#from common import *
import cx_Oracle

ResLife_MIO_1 = '192.168.0.1'
ResLife_MIO_2 = '192.168.0.1'
ResLife_MIO_3 = '192.168.0.1'
Kim_Nguyen_G5 = '192.168.0.1'
Kim_Nguyen_Air = '192.168.0.1'
Marshall_Scorcio_1 = '192.168.0.1'
Marshall_Scorcio_2 = '192.168.0.1'
Greg_Duescher_MIO = '192.168.0.1'
Joel_Kleier_MIO = '192.168.0.1'
CMF2 = '192.168.0.1'
Randy_Loch = '192.168.0.1'
Plone1 = '192.168.0.1'
Plone3 = '192.168.0.1'

def getEnrolledClassesCX (self, emplid, strm):
    request = self.REQUEST
    RESPONSE =  request.RESPONSE
    remote_addr = request.REMOTE_ADDR
    if remote_addr in [Randy_Loch, Kim_Nguyen_G5, Kim_Nguyen_Air, '192.168.0.1', '127.0.0.1', CMF2, Plone1, Plone3 ]:
        file = open('/opt/Plone-2.5.5/zeocluster/client1/Extensions/Oracle_Database_Connection_NGUYEN_PRD.txt', 'r')
        for line in file.readlines():
            if line <> "" and not line.startswith('#'):
                connString = line
        file.close()
        connection = cx_Oracle.connect(connString)
        cursor = connection.cursor()
        cursor.execute("""select c.subject, c.catalog_nbr, c.descr, c.class_section, c.crse_id, n.first_name, n.last_name, e.email_addr, i.emplid from ps_email_addresses e, ps_class_tbl c, ps_class_instr i, ps_names n where c.class_nbr in (select class_nbr from PS_STDNT_ENRL_VW where emplid = :arg1 and strm = c.strm and institution = c.institution) and c.strm = :arg2 and c.institution = 'UWOSH' and c.crse_id = i.crse_id and i.strm = c.strm and i.class_section = c.class_section and n.emplid = i.emplid and n.eff_status = 'A' and n.name_type = 'PRI' and n.effdt = (select max(effdt) from ps_names n2 where n2.emplid = n.emplid and n2.eff_status = n.eff_status and n2.name_type = n.name_type) and e.emplid = i.emplid and e_addr_type = 'CAMP'""",
                       arg1 = emplid,
                       arg2 = strm)
        retlist = []
        for column_1, column_2, column_3, column_4, column_5, column_6, column_7, column_8, column_9 in cursor:
            retlist.append([column_1, column_2, column_3, column_4, column_5, column_6, column_7, column_8, column_9,])
        myMarshaller = xmlrpclib.Marshaller()
        return myMarshaller.dumps(retlist)
