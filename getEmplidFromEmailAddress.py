# $Id: getEmplidFromEmailAddress.py,v 1.7 2008/02/06 18:43:54 kim Exp $

# Web service for ResLife MIO, work request ZCC035

import re
#from common import *
ResLife_MIO_1 = '192.168.0.1'
ResLife_MIO_2 = '192.168.0.1'
ResLife_MIO_3 = '192.168.0.1'
Kim_Nguyen_G5 = '192.168.0.1'
Kim_Nguyen_Air = '192.168.0.1'
Kim_Nguyen_MB = '192.168.0.1'
#John_Dorapalli = '192.168.0.1'
#Marshall_Scorcio_1 = '192.168.0.1'
#Marshall_Scorcio_2 = '192.168.0.1'
Greg_Duescher_MIO = '192.168.0.1'
#Joel_Kleier_MIO = '192.168.0.1'
CMF2 = '192.168.0.1'
Plone1 = '192.168.0.1'
Plone3 = '192.168.0.1'

def getEmplidFromEmailAddress (self, email):
    request = self.REQUEST
    RESPONSE =  request.RESPONSE
    remote_addr = request.REMOTE_ADDR
    if remote_addr in [ResLife_MIO_1, ResLife_MIO_2, ResLife_MIO_3, Greg_Duescher_MIO, Kim_Nguyen_G5, Kim_Nguyen_Air, Kim_Nguyen_MB, '127.0.0.1', CMF2, Plone1, Plone3]:
        if re.search(r'@uwosh.edu$', email) <> None:
            conn = getattr(self, 'Oracle_Database_Connection')
            connstr = conn.connection_string
            try:
                if not conn.connected():
                    conn.connect(connstr)
            except:
                conn.connect(connstr)
            dbc = conn()
            if connstr.find("project_success") <> -1:
                tablename = 'ps_email_addresses'
            else:
                tablename = 'ZCC035WEBSVC_VW'
            querystr = "select emplid from %s where email_addr = '%s'" % (tablename, email)
            try:
                retlist = dbc.query (querystr)
            except:
                conn.connect(connstr)
                dbc = conn()
                retlist = dbc.query (querystr)                
            if len(retlist) == 2:
                if len(retlist[1]) == 1:
                    if len(retlist[1][0]) == 1:
                        return retlist[1][0][0]
            return "No such email address"
