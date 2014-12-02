# Web service that returns campus email addresses. Matches on last name. Limits results to MAXROWS rows.

import re
import logging
logger = logging.getLogger("getMatchingEmailCX")
import cx_Oracle
import simplejson as json

Kim_Nguyen_G5 = '192.168.0.1'
Kim_Nguyen_Air = '192.168.0.1'
Kim_Nguyen_MB = '192.168.0.1'
Kim_Nguyen_MB_in_IDEA_lab = '192.168.0.1'
Kim_Nguyen_MBP_VPN = '192.168.0.1'
CMF2 = '192.168.0.1'
Plone1 = '192.168.0.1'
Plone3 = '192.168.0.1'

MAXROWS = 100

connection_file = '/opt/Plone-2.5.5/zeocluster/client1/Extensions/Oracle_Database_Connection_NGUYEN_PRD.txt'
#query_string = """select email_addr from PS_EMAIL_ADDRESSES where e_addr_type = 'CAMP' and email_addr like lower(:arg_1 || '%')"""
#query_string = """select e.email_addr, n.first_name, n.middle_name, n.last_name from PS_EMAIL_ADDRESSES e, PS_NAMES n where e.e_addr_type = 'CAMP' and e.email_addr like lower(:arg_1 || '%') and e.emplid = n.emplid and n.eff_status = 'A' and n.name_type = 'PRI' and n.effdt = (select max(n2.effdt) from PS_NAMES n2 where n2.emplid = n.emplid and n2.eff_status = 'A' and n2.name_type = 'PRI' and n2.effdt <= sysdate )"""
query_string = """select e.email_addr, n.first_name, n.middle_name, n.last_name from PS_EMAIL_ADDRESSES e, PS_NAMES n where e.e_addr_type = 'CAMP' and n.last_name_srch like upper(:arg_1 || '%') and e.emplid = n.emplid and n.eff_status = 'A' and n.name_type = 'PRI' and n.effdt = (select max(n2.effdt) from PS_NAMES n2 where n2.emplid = n.emplid and n2.eff_status = 'A' and n2.name_type = 'PRI' and n2.effdt <= sysdate )"""
limited_query_string = "select * from (%s) where ROWNUM <= %s" % (query_string, MAXROWS)

def getMatchingEmailCX (self, match, type=None):
    retlist = []
    if len(match) < 2:
        return 'match string length must be >= 2'
    request = self.REQUEST
    RESPONSE =  request.RESPONSE
    remote_addr = request.HTTP_X_FORWARDED_FOR
    if remote_addr in [Kim_Nguyen_G5, Kim_Nguyen_Air, Kim_Nguyen_MB, Kim_Nguyen_MB_in_IDEA_lab, Kim_Nguyen_MBP_VPN, '127.0.0.1', CMF2, Plone1, Plone3]:
        file = open(connection_file, 'r')
        for line in file.readlines():
            if line <> "" and not line.startswith('#'):
                connString = line
        file.close()
        connection = cx_Oracle.connect(connString)
        cursor = connection.cursor()
        #cursor.execute(query_string, arg_1 = match)
        cursor.execute(limited_query_string, arg_1 = match)
        #for column_1 in cursor:
        for column_1, column_2, column_3, column_4 in cursor:
            try:
                #retlist.append(column_1[0])
                retlist.append({'e':column_1, 'f':column_2, 'm':column_3, 'l':column_4})
            except:
                pass
        if type <> None:
            data = json.dumps(retlist)
            return data
        else:
            return retlist
