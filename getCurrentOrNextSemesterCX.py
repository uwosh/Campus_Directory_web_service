# returns the current PeopleSoft semester code, as of today
# if today is between semesters, returns the next semester code

import cx_Oracle

def getCurrentOrNextSemesterCX (self):
    file = open('/opt/Plone-2.5.5/zeocluster/client1/Extensions/Oracle_Database_Connection_NGUYEN_PRD.txt', 'r')
    for line in file.readlines():
        if line <> "" and not line.startswith('#'):
            connString = line
    file.close()
    connection = cx_Oracle.connect(connString)
    cursor = connection.cursor()
    # get the current semester code if we are within a semester
    cursor.execute("""select strm from ps_term_tbl where institution = 'UWOSH' and acad_career = 'UGRD' and term_begin_dt <= sysdate and term_end_dt >= sysdate""")
    for column_1 in cursor:
        try:
            return column_1[0]
        except:
            pass
    # otherwise get the next semester code
    cursor.execute("""select t1.strm, t1.descr from ps_term_tbl t1 where t1.institution = 'UWOSH' and t1.acad_career = 'UGRD' and t1.term_begin_dt = (select min(term_begin_dt) from ps_term_tbl t2 where t2.institution = t1.institution and t2.acad_career = t1.acad_career and term_begin_dt > sysdate)""")
    for column_1 in cursor:
        try:
            return column_1[0]
        except:
            pass
