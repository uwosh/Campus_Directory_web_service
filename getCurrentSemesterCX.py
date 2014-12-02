# returns the current PeopleSoft semester code, as of today

import cx_Oracle

Randy_Loch = '192.168.0.1'
Kim_Nguyen_G5 = '192.168.0.1'
Kim_Nguyen_Air = '192.168.0.1'
CMF2 = '192.168.0.1'
Plone1 = '192.168.0.1'
Plone3 = '192.168.0.1'

def getCurrentSemesterCX (self):
    request = self.REQUEST
    RESPONSE =  request.RESPONSE
    remote_addr = request.REMOTE_ADDR
    if remote_addr in [Plone1, CMF2, Randy_Loch, Kim_Nguyen_Air, Kim_Nguyen_G5, Plone3, '127.0.0.1', ]:
        file = open('/opt/Plone-2.5.5/zeocluster/client1/Extensions/Oracle_Database_Connection_NGUYEN_PRD.txt', 'r')
        for line in file.readlines():
            if line <> "" and not line.startswith('#'):
                connString = line
        file.close()
        connection = cx_Oracle.connect(connString)
        cursor = connection.cursor()
        cursor.execute("""select strm from ps_term_tbl where institution = 'UWOSH' and acad_career = 'UGRD' and term_begin_dt <= sysdate and term_end_dt >= sysdate""")
        for column_1 in cursor:
            try:
                return column_1[0]
            except:
                pass
        return "error: no semester code found matching current date"
