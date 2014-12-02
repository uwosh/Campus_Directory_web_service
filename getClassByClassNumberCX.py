import logging
logger = logging.getLogger("getClassByClassNumberCX")
import cx_Oracle
import xmlrpclib

www1_webcluster_uwosh_edu = '192.168.0.1'
Kim_Nguyen_G5 = '192.168.0.1'
Maccabee_Levine_laptop = '192.168.0.1'

def getClassByClassNumberCX (self, class_nbr, strm):
    request = self.REQUEST
    RESPONSE =  request.RESPONSE
    remote_addr = request.REMOTE_ADDR
    if remote_addr in [www1_webcluster_uwosh_edu, Kim_Nguyen_G5, '127.0.0.1', Maccabee_Levine_laptop]:
        file = open('/opt/Plone-2.5.5/zeocluster/client1/Extensions/Oracle_Database_Connection_ZCC041WEBSVCUSER.txt', 'r')
        for line in file.readlines():
            if line <> "" and not line.startswith('#'):
                connString = line
        file.close()
        connection = cx_Oracle.connect(connString)
        cursor = connection.cursor()
        cursor.execute("""select * from PS_ZCC041WEBSVCVW where class_nbr = :arg_1 and strm = :arg_2""",
                       arg_1 = class_nbr,
                       arg_2 = strm)
        myMarshaller = xmlrpclib.Marshaller()
        for column_1, column_2, column_3, column_4, column_5, column_6, column_7, column_8, column_9, column_10, column_11 in cursor:
            return myMarshaller.dumps([column_1, column_2, column_3, column_4, column_5, column_6, column_7, column_8, column_9, column_10, column_11,])
