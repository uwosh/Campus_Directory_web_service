# returns the end date of the current PeopleSoft 14W session (Sept. -
# Dec., and Feb.-May-ish), ie. not interim sessions and not the summer
# session

import cx_Oracle

Kim_Nguyen_G5 = '192.168.0.1'
Kim_Nguyen_Air = '192.168.0.1'
CMF2 = '192.168.0.1'
Plone1 = '192.168.0.1'
Plone3 = '192.168.0.1'

def get14WSessionUgradEndDateCX (self):
    request = self.REQUEST
    RESPONSE =  request.RESPONSE
    remote_addr = request.REMOTE_ADDR
    if remote_addr in [Plone1, CMF2, Kim_Nguyen_Air, Kim_Nguyen_G5, Plone3, '127.0.0.1', ]:
        file = open('/opt/Plone-2.5.5/zeocluster/client1/Extensions/Oracle_Database_Connection_NGUYEN_PRD.txt', 'r')
        for line in file.readlines():
            if line <> "" and not line.startswith('#'):
                connString = line
        file.close()
        connection = cx_Oracle.connect(connString)
        cursor = connection.cursor()
        cursor.execute("""select sess_end_dt from ps_session_tbl where sess_begin_dt <= sysdate and sess_end_dt >= sysdate and acad_career = 'UGRD' and session_code = '14W'""")
        for column_1 in cursor:
            try:
                return str(column_1[0])
            except:
                return "not a 14W session"
        return "not a 14W session"
