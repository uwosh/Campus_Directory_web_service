# $Id$

# Web service for campus directory project

import re
import xmlrpclib
Randy_Loch = '192.168.0.1'
Kim_Nguyen_G5 = '192.168.0.1'

def CampusDirectoryZEM001VALUOVW (self, org_unit='None'):
    request = self.REQUEST
    RESPONSE =  request.RESPONSE
    remote_addr = request.REMOTE_ADDR
    if remote_addr in [Randy_Loch, Kim_Nguyen_G5, '127.0.0.1', ]:
        conn = getattr(self, 'Oracle_Database_Connection_Campus_Directory')
        connstr = conn.connection_string
        try:
            if not conn.connected():
                conn.connect(connstr)
        except:
            conn.connect(connstr)
        dbc = conn()
        tablename = 'PS_ZEM001VALUOVW'
        if org_unit == 'None':
            querystr = "select * from %s" % (tablename)
        else:
            querystr = "select * from %s where z_univ_org = '%s'" % (tablename, org_unit)
        try:
            retlist = dbc.query (querystr)
        except:
            conn.connect(connstr)
            dbc = conn()
            retlist = dbc.query (querystr)                
        myMarshaller = xmlrpclib.Marshaller()
        return myMarshaller.dumps(retlist[1])
