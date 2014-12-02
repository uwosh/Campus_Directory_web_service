# $Id$

# Web service for campus directory project

import re
import xmlrpclib
Kim_Nguyen_G5 = '192.168.0.1'

def CampusDirectoryZEM001VALPHVW (self, phone_extension):
    request = self.REQUEST
    RESPONSE =  request.RESPONSE
    remote_addr = request.REMOTE_ADDR
    if remote_addr in ['192.168.0.1', Kim_Nguyen_G5, '127.0.0.1', ]:
        conn = getattr(self, 'Oracle_Database_Connection_Campus_Directory')
        connstr = conn.connection_string
        try:
            if not conn.connected():
                conn.connect(connstr)
        except:
            conn.connect(connstr)
        dbc = conn()
        tablename = 'PS_ZEM001VALPHVW'
        querystr = "select * from %s where z_tb_line = '%s'" % (tablename, phone_extension)
        try:
            retlist = dbc.query (querystr)
        except:
            conn.connect(connstr)
            dbc = conn()
            retlist = dbc.query (querystr)                
        myMarshaller = xmlrpclib.Marshaller()
        return myMarshaller.dumps(retlist[1])
