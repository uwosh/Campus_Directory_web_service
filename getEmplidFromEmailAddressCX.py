# Web service for ResLife MIO, work request ZCC035

import re
import logging
logger = logging.getLogger("getClassByClassNumberCX")
import cx_Oracle

ResLife_MIO_1 = '192.168.0.1'
ResLife_MIO_2 = '192.168.0.1'
ResLife_MIO_3 = '192.168.0.1'
Kim_Nguyen_G5 = '192.168.0.1'
Kim_Nguyen_Air = '192.168.0.1'
Kim_Nguyen_MB = '192.168.0.1'
Kim_Nguyen_MB_in_IDEA_lab = '192.168.0.1'
John_Hren_MBP_IDEA_lab = '192.168.0.1'
#Marshall_Scorcio_1 = '192.168.0.1'
#Marshall_Scorcio_2 = '192.168.0.1'
Greg_Duescher_MIO = '192.168.0.1'
#Joel_Kleier_MIO = '192.168.0.1'
CMF2 = '192.168.0.1'
Plone1 = '192.168.0.1'
Plone3 = '192.168.0.1'

# connection_file = '/opt/Plone-2.5.5/zeocluster/client1/Extensions/Oracle_Database_Connection.txt'
# query_string = """select emplid from ZCC035WEBSVC_VW where email_addr = :arg_1"""

connection_file = '/opt/Plone-2.5.5/zeocluster/client1/Extensions/Oracle_Database_Connection_NGUYEN_PRD.txt'
query_string = """select emplid from PS_EMAIL_ADDRESSES where e_addr_type = 'CAMP' and email_addr = :arg_1"""

def getEmplidFromEmailAddressCX (self, email):
    request = self.REQUEST
    RESPONSE =  request.RESPONSE
    remote_addr = request.REMOTE_ADDR
    if remote_addr in [ResLife_MIO_1, ResLife_MIO_2, ResLife_MIO_3, Greg_Duescher_MIO, Kim_Nguyen_G5, Kim_Nguyen_Air, Kim_Nguyen_MB, Kim_Nguyen_MB_in_IDEA_lab, John_Hren_MBP_IDEA_lab, '127.0.0.1', CMF2, Plone1, Plone3]:
        if re.search(r'@uwosh.edu$', email) <> None:
            file = open(connection_file, 'r')
            for line in file.readlines():
                if line <> "" and not line.startswith('#'):
                    connString = line
            file.close()
            connection = cx_Oracle.connect(connString)
            cursor = connection.cursor()
            cursor.execute(query_string,
                           arg_1 = email)
            for column_1 in cursor:
                try:
                    return column_1[0]
                except:
                    return "No such email address"
            return "No such email address"
