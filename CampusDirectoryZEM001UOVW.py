# $Id$

# Web service for campus directory project

import re
import xmlrpclib
#from common import *
ResLife_MIO_1 = '192.168.0.1'
ResLife_MIO_2 = '192.168.0.1'
ResLife_MIO_3 = '192.168.0.1'
Kim_Nguyen_G5 = '192.168.0.1'
Kim_Nguyen_Air = '192.168.0.1'
John_Dorapalli = '192.168.0.1'
Marshall_Scorcio_1 = '192.168.0.1'
Marshall_Scorcio_2 = '192.168.0.1'
Greg_Duescher_MIO = '192.168.0.1'
Joel_Kleier_MIO = '192.168.0.1'

def CampusDirectoryZEM001UOVW (self, emplid):
    request = self.REQUEST
    RESPONSE =  request.RESPONSE
    remote_addr = request.REMOTE_ADDR
    if remote_addr in ['192.168.0.1', Kim_Nguyen_G5, Marshall_Scorcio_1, Marshall_Scorcio_2, Kim_Nguyen_Air, '127.0.0.1', ]:
        conn = getattr(self, 'Oracle_Database_Connection_Campus_Directory')
        connstr = conn.connection_string
        try:
            if not conn.connected():
                conn.connect(connstr)
        except:
            conn.connect(connstr)
        dbc = conn()
        tablename = 'PS_ZEM001UOVW'
        querystr = "select * from %s where emplid = '%s'" % (tablename, emplid)
        try:
            retlist = dbc.query (querystr)
        except:
            conn.connect(connstr)
            dbc = conn()
            retlist = dbc.query (querystr)                
        myMarshaller = xmlrpclib.Marshaller()
        return myMarshaller.dumps(retlist[1])
