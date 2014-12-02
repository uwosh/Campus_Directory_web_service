# Web service for campus directory project

import cx_Oracle
import xmlrpclib

Randy_Loch = '192.168.0.1'
Kim_Nguyen_G5 = '192.168.0.1'

def CampusDirectoryZEM001VALUOVWCX (self, org_unit='None'):
    request = self.REQUEST
    RESPONSE =  request.RESPONSE
    remote_addr = request.REMOTE_ADDR
    if remote_addr in [Randy_Loch, Kim_Nguyen_G5, '127.0.0.1', ]:
        file = open('/opt/Plone-2.5.5/zeocluster/client1/Extensions/Oracle_Database_Connection_Campus_Directory.txt', 'r')
        for line in file.readlines():
            if line <> "" and not line.startswith('#'):
                connString = line
        file.close()
        connection = cx_Oracle.connect(connString)
        cursor = connection.cursor()
        if org_unit == 'None':
            cursor.execute("""select * from PS_ZEM001VALUOVW """)
        else:
            cursor.execute("""select * from PS_ZEM001VALUOVW where z_univ_org = :arg1""", arg1=org_unit)
        retlist = []
        for c1, c2 in cursor:
            retlist.append([c1, c2,])
        myMarshaller = xmlrpclib.Marshaller()
        return myMarshaller.dumps(retlist)
