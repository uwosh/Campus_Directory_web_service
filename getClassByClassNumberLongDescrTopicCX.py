import logging
logger = logging.getLogger("getClassByClassNumberLongDescrTopicCX")
import cx_Oracle
import xmlrpclib

www1_webcluster_uwosh_edu = '192.168.0.1'
Kim_Nguyen_G5 = '192.168.0.1'
Maccabee_Levine_laptop = '192.168.0.1'
polk_uwosh_edu = '192.168.0.1'
wwwtest_polk_uwosh_edu = '192.168.0.1'

# examples with topics:
# https://ws.it.uwosh.edu/getClassByClassNumberLongDescrTopicCX?class_nbr=40684&strm=0645
# https://ws.it.uwosh.edu/getClassByClassNumberLongDescrTopicCX?class_nbr=40687&strm=0645
# https://ws.it.uwosh.edu/getClassByClassNumberLongDescrTopicCX?class_nbr=40691&strm=0645
# https://ws.it.uwosh.edu/getClassByClassNumberLongDescrTopicCX?class_nbr=40699&strm=0645
# example without topic:
# https://ws.it.uwosh.edu/getClassByClassNumberLongDescrTopicCX?class_nbr=40810&strm=0645

def getClassByClassNumberLongDescrTopicCX (self, class_nbr, strm):
    request = self.REQUEST
    RESPONSE =  request.RESPONSE
    remote_addr = request.REMOTE_ADDR
    if remote_addr in [www1_webcluster_uwosh_edu, Kim_Nguyen_G5, '127.0.0.1', Maccabee_Levine_laptop, polk_uwosh_edu, wwwtest_polk_uwosh_edu]:
        file = open('/opt/Plone-2.5.5/zeocluster/client1/Extensions/Oracle_Database_Connection_NGUYEN_PRD.txt', 'r')
        for line in file.readlines():
            if line <> "" and not line.startswith('#'):
                connString = line
        file.close()
        connection = cx_Oracle.connect(connString)
        cursor = connection.cursor()
        cursor.execute("""SELECT C.SUBJECT, C.CATALOG_NBR, C.DESCR, C.CLASS_SECTION,
     C.CRSE_ID, C.CLASS_NBR, C.STRM, N.FIRST_NAME, N.LAST_NAME,
I.EMPLID, e.email_addr, cc.course_title_long, t.descr
FROM PS_CLASS_TBL C left join ps_crse_topics t on c.crse_id = t.crse_id and c.crs_topic_id = t.crs_topic_id , PS_CLASS_INSTR I, PS_NAMES N, ps_email_addresses e, ps_crse_catalog cc 
WHERE C.INSTITUTION = 'UWOSH'
AND I.CRSE_ID = C.CRSE_ID
AND I.STRM = C.STRM
AND I.CLASS_SECTION = C.CLASS_SECTION
AND N.EMPLID = I.EMPLID
AND N.EFF_STATUS = 'A'
AND N.NAME_TYPE = 'PRI'
AND N.EFFDT = (SELECT MAX(EFFDT) FROM PS_NAMES N2 WHERE N2.EMPLID = N.EMPLID AND N2.EFF_STATUS = N.EFF_STATUS AND N2.NAME_TYPE = N.NAME_TYPE)
and e.emplid = i.emplid and e_addr_type = 'CAMP' 
and c.crse_id = cc.crse_id and cc.effdt = (select max(effdt) from ps_crse_catalog where crse_id = cc.crse_id and eff_status = 'A') and cc.eff_status = 'A'
     and c.class_nbr = :arg_1 and c.strm = :arg_2 and rownum < 2 order by t.effdt desc""",
                       arg_1 = class_nbr,
                       arg_2 = strm)
        myMarshaller = xmlrpclib.Marshaller(allow_none=1)
        for column_1, column_2, column_3, column_4, column_5, column_6, column_7, column_8, column_9, column_10, column_11, column_12, column_13 in cursor:
            return myMarshaller.dumps([column_1, column_2, column_3, column_4, column_5, column_6, column_7, column_8, column_9, column_10, column_11, column_12, column_13])
