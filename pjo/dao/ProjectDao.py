import logging
from django.db import connection
from django.db.models import Max
from django.shortcuts import get_object_or_404
from pjo.models import Project
from pjo.models import Raw
from pjo.models import RawScan
from pjo.util.PjoDBUtil import DBUtil

dbLogger = logging.getLogger("dba")
errLogger = logging.getLogger("errLog")


class ProjectDao(object):

    def __init__(self):
        pass

    """
    ==============================================================================
     Project
    ==============================================================================
    """

    # ==============================================================================
    #  Select Project Object
    # ==============================================================================
    @staticmethod
    def select_project_object(project_id):

        project = get_object_or_404(Project, pk=project_id)

        return project

    # ==============================================================================
    #  Insert Project
    # ==============================================================================
    @staticmethod
    def insert_project(dic_project):

        # project_id
        project_id = Project.objects.all().aggregate(Max("project_id"))
        str_project_id = project_id['project_id__max']

        if str_project_id is None:
            str_project_id = "1"
            str_project_id = str_project_id.zfill(4)
        else:
            str_project_id = str(int(str_project_id) + 1)
            str_project_id = str_project_id.zfill(4)

        dbLogger.debug("strProjectId====[" + str_project_id + "]")

        str_animal_strain = dic_project['animalStrain']
        str_animal_strain = str_animal_strain[1:2]

        project = Project(project_id=str_project_id,
                          initial_nm=dic_project['piInit'],
                          animal_type=dic_project['animalType'],
                          strain_type=str_animal_strain,
                          classification=dic_project['classification'],
                          year="20"+dic_project['year'],
                          pi_first_nm=dic_project['firstName'],
                          pi_last_nm=dic_project['lastName'],
                          project_aim=dic_project['projectAim'],
                          reg_id=dic_project['regId'],
                          reg_date=dic_project['regDate'])
        dbLogger.debug(connection.queries[-1])
        project.save()

        return str_project_id

    # ==============================================================================
    #  Select Project List with inquiry condition
    # ==============================================================================
    @staticmethod
    def select_project_list(context):

        # parameter list
        param_list = list()

        # make query
        query_list = list()

        query_list.append("SELECT A.PROJECT_ID                \n")
        query_list.append("     , A.INITIAL_NM                \n")
        query_list.append("     , A.ANIMAL_TYPE               \n")
        query_list.append("     , (SELECT CODE_NM             \n")
        query_list.append("          FROM PJO_CODE            \n")
        query_list.append("         WHERE GROUP_ID = '002'    \n")
        query_list.append("           AND CODE_ID = A.ANIMAL_TYPE) AS ANIMAL_NM \n")
        query_list.append("     , (SELECT CODE_NM             \n")
        query_list.append("          FROM PJO_DB.PJO_CODE     \n")
        query_list.append("         WHERE GROUP_ID = '003'    \n")
        query_list.append("           AND CODE_ID = CONCAT(A.ANIMAL_TYPE, A.STRAIN_TYPE)) AS STRAIN_NM \n")
        query_list.append("     , A.STRAIN_TYPE               \n")
        query_list.append("     , A.CLASSIFICATION            \n")
        query_list.append("     , A.YEAR                      \n")
        query_list.append("     , CONCAT(A.PI_FIRST_NM, A.PI_LAST_NM) AS RESEARCHER_NM \n")
        query_list.append("     , A.PROJECT_AIM               \n")
        query_list.append("     , A.MODIFIABLE                \n")
        query_list.append("     , A.REG_DATE                  \n")
        query_list.append("  FROM PJO_DB.PJO_PROJECT A        \n")
        query_list.append(" WHERE 1=1                         \n")

        if 'txtPIInit' in context and context['txtPIInit'] != "":
            query_list.append("   AND A.INITIAL_NM = %s \n")
            param_list.append(context['txtPIInit'])
        if 'txtPIName' in context and context['txtPIName'] != "":
            query_list.append("   AND (A.PI_FIRST_NM LIKE %s OR A.PI_LAST_NM LIKE %s )\n")
            param_list.append("%" + context['txtPIName'] + "%")
            param_list.append("%" + context['txtPIName'] + "%")
        if 'selAnimalType' in context and context['selAnimalType'] != "":
            query_list.append("   AND A.ANIMAL_TYPE = %s \n")
            param_list.append(context['selAnimalType'])
        if 'selYear' in context and context['selYear'] != "":
            query_list.append("   AND A.YEAR = %s \n")
            param_list.append("20" + context['selYear'])
        if 'txtProjectAim' in context and context['txtProjectAim'] != "":
            query_list.append("   AND A.PROJECT_AIM LIKE %s \n")
            param_list.append("%" + context['txtProjectAim'] + "%")

        query_list.append(" ORDER BY A.PROJECT_ID DESC \n")

        # get data
        with connection.cursor() as c:
            try:
                c.execute(''.join(query_list), param_list)
                result_list = DBUtil().f_dictfetchall(c)
                # dbLogger.debug(''.join(query_list))
            finally:
                c.close()
        return result_list

    # ==============================================================================
    #  Update Project
    # ==============================================================================
    @staticmethod
    def update_project(dic_project):
        project = ProjectDao.select_project_object(dic_project["projectId"])
        project.pi_first_nm = dic_project['firstName']
        project.pi_last_nm = dic_project['lastName']
        project.year = dic_project['year']
        project.project_aim = dic_project['projectAim']
        project.save()
        dbLogger.info(connection.queries[-1])

    # ==============================================================================
    #  Insert Raw
    # ==============================================================================
    @staticmethod
    def insert_raw(dic_raw):

        raw = Raw(raw_folder_nm=dic_raw['rawFolderNm'],
                  raw_save_date=dic_raw['rawSaveDate'],
                  reg_id=dic_raw['regId'],
                  reg_date=dic_raw['regDate'])
        dbLogger.debug(connection.queries[-1])
        raw.save()

    # ==============================================================================
    #  Select Raw List with inquiry condition
    # ==============================================================================
    @staticmethod
    def select_raw_list(context):

        # parameter list
        param_list = list()

        # make query
        query_list = list()

        query_list.append("SELECT A.ID                 \n")
        query_list.append("     , A.RAW_FOLDER_NM      \n")
        query_list.append("     , A.RAW_SAVE_DATE      \n")
        query_list.append("     , A.RAW_SUBJECT_ID     \n")
        query_list.append("     , A.RAW_RESEARCHER     \n")
        query_list.append("     , A.RAW_SPECIMEN       \n")
        query_list.append("     , A.RAW_GENDER         \n")
        query_list.append("     , A.RAW_AGE            \n")
        query_list.append("     , A.RAW_WEIGHT         \n")
        query_list.append("     , A.RAW_DELIVERY_DATE  \n")
        query_list.append("     , A.BACKUP_YN          \n")
        query_list.append("     , A.CONVERT_YN         \n")
        query_list.append("  FROM PJO_DB.PJO_RAW A     \n")
        query_list.append(" WHERE 1=1                  \n")

        if 'txtRawFileNm' in context and context['txtRawFileNm'] != "":
            query_list.append("   AND A.RAW_FOLDER_NM LIKE %s \n")
            param_list.append("%" + context['txtRawFileNm'] + "%")
        if 'txtStartDate' in context and context['txtStartDate'] != "":
            query_list.append("   AND A.RAW_SAVE_DATE BETWEEN %s AND %s \n")
            param_list.append(context['txtStartDate'])
            param_list.append(context['txtEndDate'])
        if 'selConvertYn' in context and context['selConvertYn'] != "":
            query_list.append("   AND A.CONVERT_YN = %s \n")
            param_list.append(context['selConvertYn'])
        if 'selBackupYn' in context and context['selBackupYn'] != "":
            query_list.append("   AND A.BACKUP_YN = %s \n")
            param_list.append(context['selBackupYn'])
        query_list.append(" ORDER BY A.ID DESC \n")

        # get data
        with connection.cursor() as c:
            try:
                c.execute(''.join(query_list), param_list)
                result_list = DBUtil().f_dictfetchall(c)
                dbLogger.debug(''.join(query_list))
                dbLogger.debug(param_list)
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






