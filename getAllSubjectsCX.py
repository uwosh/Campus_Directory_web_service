# getAllSubjectsCX 

import re
import xmlrpclib
import cx_Oracle

Kim_Nguyen_G5 = '192.168.0.1'
Kim_Nguyen_iMac = '192.168.0.1'
Kim_Nguyen_MacBook = '192.168.0.1'
Plone1 = '192.168.0.1'
Plone3 = '192.168.0.1'

def getAllSubjectsCX (self, usexml):
    request = self.REQUEST
    RESPONSE =  request.RESPONSE
    remote_addr = request.REMOTE_ADDR
    if remote_addr in [Kim_Nguyen_iMac, Kim_Nguyen_MacBook, '127.0.0.1', Plone3 ]:
        file = open('/opt/Plone-2.5.5/zeocluster/client1/Extensions/Oracle_Database_Connection_NGUYEN_PRD.txt', 'r')
        for line in file.readlines():
            if line <> "" and not line.startswith('#'):
                connString = line
        file.close()
        connection = cx_Oracle.connect(connString)
        cursor = connection.cursor()
        #cursor.execute("""select distinct(subject) from ps_class_tbl order by subject""")
        cursor.execute("""select distinct subject, descr from ps_subject_tbl s1 where s1.eff_status = 'A' and s1.effdt = (select max(s2.effdt) from ps_subject_tbl s2 where s1.subject = s2.subject and s2.eff_status = 'A' and s1.institution = s2.institution and s1.acad_org = s2.acad_org)""")
        retlist = []
        for column_1, column_2 in cursor:
            retlist.append([column_1, column_2,])
        if usexml == "0":
            return retlist
        else:
            myMarshaller = xmlrpclib.Marshaller()
            return myMarshaller.dumps(retlist)
