# getCatalogNumbersByTermAndSubjectJSONPCX

import re
# try:
#     import json
# except ImportError:
#     import simplejson as json
import simplejson as json
import cx_Oracle

Kim_Nguyen_G5 = '192.168.0.1'
Kim_Nguyen_iMac = '192.168.0.1'
Kim_Nguyen_MacBook = '192.168.0.1'
Kim_Nguyen_MacBook_IDEA_lab = '192.168.0.1'
Plone1 = '192.168.0.1'
Plone3 = '192.168.0.1'
Joel_Herron_iMac = '192.168.0.1'
ws_it_uwosh_edu = '192.168.0.1'
Maccabee_Levine = '192.168.0.1'
MIO_Helios_Server = '192.168.0.1'
David_Hietpas = '192.168.0.1'
John_Hren_MBP = '192.168.0.1'
John_Hren_MBP_IDEA_lab = '192.168.0.1'

def getCatalogNumbersByTermAndSubjectJSONPCX(self, strm, subject, callback="?"):
    request = self.REQUEST
    RESPONSE =  request.RESPONSE
    remote_addr = request.REMOTE_ADDR
    if remote_addr in [Kim_Nguyen_iMac, '127.0.0.1', Plone3, ws_it_uwosh_edu, Kim_Nguyen_MacBook, Kim_Nguyen_G5, Kim_Nguyen_MacBook_IDEA_lab, John_Hren_MBP, John_Hren_MBP_IDEA_lab]:
        file = open('/opt/Plone-2.5.5/zeocluster/client2/Extensions/Oracle_Database_Connection_NGUYEN_PRD.txt', 'r')
        for line in file.readlines():
            if line <> "" and not line.startswith('#'):
                connString = line
        file.close()
        connection = cx_Oracle.connect(connString)
        cursor = connection.cursor()
        cursor.execute("""
select 
 distinct c.catalog_nbr
from
 ps_class_tbl c
where 
 c.strm = :arg1
 and c.institution = 'UWOSH' 
 and c.subject = :arg2
""",
                       arg1 = strm, arg2 = subject)
        retlist = []
        for column_1 in cursor:
            retlist.append([column_1, ])
        data = json.dumps(retlist)
        #request.response.setHeader('Content-Type', 'application/json')
        return callback + '(' + data + ');'
