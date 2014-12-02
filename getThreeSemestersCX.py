import cx_Oracle
import xmlrpclib

def getThreeSemestersCX (self):
    file = open('/opt/Plone-2.5.5/zeocluster/client1/Extensions/Oracle_Database_Connection_NGUYEN_PRD.txt', 'r')
    for line in file.readlines():
        if line <> "" and not line.startswith('#'):
            connString = line
    file.close()
    connection = cx_Oracle.connect(connString)
    cursor = connection.cursor()
    cursor.execute("""select * from (select strm, descr from ps_term_tbl where institution = 'UWOSH' and acad_career = 'UGRD' and term_begin_dt <= sysdate and term_end_dt >= sysdate union select t1.strm, t1.descr from ps_term_tbl t1 where t1.institution = 'UWOSH' and t1.acad_career = 'UGRD' and t1.term_begin_dt >= (select min(term_begin_dt) from ps_term_tbl t2 where t2.institution = t1.institution and t2.acad_career = t1.acad_career and term_begin_dt > sysdate)) where rownum <= 3""")
    retlist = []
    for column_1, column_2 in cursor:
        retlist.append([column_1, column_2,  ])
    myMarshaller = xmlrpclib.Marshaller(allow_none=True)
    return myMarshaller.dumps(retlist)
