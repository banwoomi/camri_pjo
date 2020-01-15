import logging
from django.db import connection
from django.db.models import Max
from django.shortcuts import get_object_or_404
from pjo.models import Raw
from pjo.models import RawScan
from pjo.models import RawRecon
from pjo.util.PjoDBUtil import DBUtil

dbLogger = logging.getLogger("dba")
errLogger = logging.getLogger("errLog")


class RawDao(object):

    def __init__(self):
        pass

    # ==============================================================================
    #  Insert Raw
    # ==============================================================================
    @staticmethod
    def insert_raw(dic_raw):

        raw = Raw(raw_folder_nm=dic_raw['rawFolderNm'],
                  raw_save_date=dic_raw['rawSaveDate'],
                  raw_subject_id=dic_raw['rawSubjectId'],
                  raw_researcher=dic_raw['rawResearcher'],
                  raw_specimen=dic_raw['rawSpecimen'],
                  raw_gender=dic_raw['rawGender'],
                  raw_weight=dic_raw['rawWeight'],
                  raw_delivery_date=dic_raw['rawDeliveryDate'],
                  reg_id=dic_raw['regId'],
                  reg_date=dic_raw['regDate'])

        dbLogger.debug("\n{}".format(connection.queries[-1]))
        dbLogger.debug(dic_raw)
        raw.save()

        return raw.id

    # ==============================================================================
    #  Insert RawScan
    # ==============================================================================
    @staticmethod
    def insert_raw_scan(dic_raw_scan):

        raw_scan = RawScan(raw_id=dic_raw_scan['rawId'],
                           scan_num=dic_raw_scan['scan_num'],
                           method=dic_raw_scan['method'][0:10],
                           tr=dic_raw_scan['tr'],
                           te=dic_raw_scan['te'],
                           band_width=dic_raw_scan['band_width'],
                           flip_angle=dic_raw_scan['flip_angle'],
                           fid=dic_raw_scan['fid'],
                           reg_id=dic_raw_scan['regId'],
                           reg_date=dic_raw_scan['regDate'])

        dbLogger.debug("\n{}".format(connection.queries[-1]))
        dbLogger.debug(dic_raw_scan)
        raw_scan.save()

        return raw_scan.id

    # ==============================================================================
    #  Insert RawRecon
    # ==============================================================================
    @staticmethod
    def insert_raw_recon(dic_raw_recon):

        raw_recon = RawRecon(raw_scan_id=dic_raw_recon["rawScanId"],
                             recon_num=dic_raw_recon["reconNum"],
                             byte_order=dic_raw_recon["byteOrder"],
                             word_type=dic_raw_recon["wordType"],
                             resolution=dic_raw_recon["resolution"],
                             matrix=dic_raw_recon["matrix"],
                             fov=dic_raw_recon["fov"],
                             thickness=dic_raw_recon['thickness'],
                             reg_id=dic_raw_recon['regId'],
                             reg_date=dic_raw_recon['regDate'])
        dbLogger.debug("\n{}".format(connection.queries[-1]))
        dbLogger.debug(dic_raw_recon)
        raw_recon.save()

        return raw_recon.id

    # ==============================================================================
    #  Select Raw List with inquiry condition
    # ==============================================================================
    @staticmethod
    def select_raw_list(context):

        # parameter list
        param_list = list()

        # make query
        query_list = list()

        query_list.append("SELECT A.ID                                 \n")
        query_list.append("     , ISNULL(B.RAW_ID) AS MAP_YN           \n")
        query_list.append("     , A.RAW_FOLDER_NM                      \n")
        query_list.append("     , A.RAW_SAVE_DATE                      \n")
        query_list.append("     , A.RAW_SUBJECT_ID                     \n")
        query_list.append("     , A.RAW_RESEARCHER                     \n")
        query_list.append("     , A.RAW_SPECIMEN                       \n")
        query_list.append("     , A.RAW_GENDER                         \n")
        query_list.append("     , A.RAW_AGE                            \n")
        query_list.append("     , A.RAW_WEIGHT                         \n")
        query_list.append("     , A.RAW_DELIVERY_DATE                  \n")
        query_list.append("     , (SELECT COUNT(*)                     \n")
        query_list.append("          FROM PJO_DB.PJO_RAWSCAN B         \n")
        query_list.append("         WHERE A.ID = B.RAW_ID) AS CNT      \n")
        query_list.append("  FROM PJO_DB.PJO_RAW A                     \n")
        query_list.append("  LEFT OUTER JOIN                           \n")
        query_list.append("       (SELECT SUB.RAW_ID, SUB.SUBJECT_NM   \n")
        query_list.append("		  FROM PJO_DB.PJO_PROJECT PRJ            \n")
        query_list.append("			 , PJO_DB.PJO_SUBJECT SUB              \n")
        query_list.append("		 WHERE PRJ.PROJECT_ID = SUB.PROJECT_ID   \n")
        query_list.append("		   AND PRJ.PROJECT_ID = %s ) B           \n")
        query_list.append("   ON A.ID = B.RAW_ID                       \n")
        query_list.append(" WHERE 1=1                                  \n")

        param_list.append(context['navProjectId'])

        if 'txtRawFileNm' in context and context['txtRawFileNm'] != "":
            query_list.append("   AND A.RAW_FOLDER_NM LIKE %s \n")
            param_list.append("%" + context['txtRawFileNm'] + "%")
        if 'txtStartDate' in context and context['txtStartDate'] != "":
            query_list.append("   AND A.RAW_SAVE_DATE BETWEEN %s AND %s \n")
            param_list.append(context['txtStartDate'])
            param_list.append(context['txtEndDate'])
        query_list.append(" ORDER BY B.RAW_ID DESC, A.ID DESC          \n")

        # get data
        with connection.cursor() as c:
            try:
                c.execute(''.join(query_list), param_list)
                result_list = DBUtil().f_dict_fetchall(c)
                dbLogger.debug(''.join(query_list))
                # dbLogger.debug(param_list)
            finally:
                c.close()
        return result_list

    # ==============================================================================
    #  Select Raw List
    # ==============================================================================
    @staticmethod
    def select_raw_list_by_name(raw_folder_nm):
        raw_list = Raw.objects.filter(raw_folder_nm=raw_folder_nm)
        return raw_list

    # ==============================================================================
    #  Select Raw Object
    # ==============================================================================
    @staticmethod
    def select_raw_object(raw_id):
        raw = get_object_or_404(Raw, pk=raw_id)
        return raw

    # ==============================================================================
    #  Select Rawscan, Rawrecon List
    # ==============================================================================
    @staticmethod
    def select_raw_scan_list(raw_id, raw_scan_id, raw_recon_id):

        # parameter list
        param_list = list()

        # make query
        query_list = list()
        query_list.append("SELECT A.RAW_ID                                      \n")
        query_list.append("     , A.ID AS RAW_SCAN_ID                           \n")
        query_list.append("     , A.SCAN_NUM                                    \n")
        query_list.append("     , A.METHOD                                      \n")
        query_list.append("     , A.TE, A.TR, A.BAND_WIDTH, A.FLIP_ANGLE        \n")
        query_list.append("     , CASE WHEN A.FID = 'Y' THEN 'Complete'         \n")
        query_list.append("            WHEN A.FID = 'N' THEN 'Interrupt'        \n")
        query_list.append("       END AS FID                                    \n")
        query_list.append("     , IFNULL(B.ID, '') RAW_RECON_ID                 \n")
        query_list.append("     , IFNULL(B.RECON_NUM, '') RECON_NO              \n")
        query_list.append("     , IFNULL(B.FOV, '') FOV                         \n")
        query_list.append("     , IFNULL(B.MATRIX, '') MATRIX                   \n")
        query_list.append("     , IFNULL(B.RESOLUTION, '') RESOLUTION           \n")
        query_list.append("     , IFNULL(B.THICKNESS, '') THICKNESS             \n")
        query_list.append("     , IFNULL(B.BYTE_ORDER, '') BYTE_ORDER           \n")
        query_list.append("     , IFNULL(B.WORD_TYPE, '') WORD_TYPE             \n")
        query_list.append("  FROM PJO_DB.PJO_RAWSCAN A                          \n")
        query_list.append("  LEFT OUTER JOIN PJO_DB.PJO_RAWRECON B              \n")
        query_list.append("    ON A.ID = B.RAW_SCAN_ID                          \n")
        query_list.append(" WHERE A.RAW_ID = %s                                 \n")
        param_list.append(raw_id)

        if raw_scan_id != "":
            query_list.append("   AND A.ID = %s \n")
            param_list.append(raw_scan_id)
        if raw_recon_id != "":
            query_list.append("   AND B.ID = %s \n")
            param_list.append(raw_recon_id)

        query_list.append(" ORDER BY A.ID ASC                                   \n")

        # get data
        with connection.cursor() as c:
            try:
                c.execute(''.join(query_list), param_list)
                result_list = DBUtil().f_dict_fetchall(c)
                dbLogger.debug(''.join(query_list))
            finally:
                c.close()
        return result_list
