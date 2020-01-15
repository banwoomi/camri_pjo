import logging
from django.db import connection
from django.db.models import Max
from django.shortcuts import get_object_or_404
from pjo.models import Project
from pjo.models import Subject
from pjo.models import Session
from pjo.models import Scan
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
    #  Select Subject Object
    # ==============================================================================
    @staticmethod
    def select_subject_object(subject_id):

        subject = get_object_or_404(Subject, pk=subject_id)

        return subject

    # ==============================================================================
    #  Select Session Object
    # ==============================================================================
    @staticmethod
    def select_session_object(session_id):

        session = get_object_or_404(Session, pk=session_id)

        return session

    # ==============================================================================
    #  Select Scan Object
    # ==============================================================================
    @staticmethod
    def select_scan_object(scan_id):

        scan = get_object_or_404(Scan, pk=scan_id)

        return scan

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
                          year=dic_project['year'],
                          pi_first_nm=dic_project['firstName'],
                          pi_last_nm=dic_project['lastName'],
                          project_aim=dic_project['projectAim'],
                          reg_id=dic_project['regId'],
                          reg_date=dic_project['regDate'])
        dbLogger.debug("\n{}".format(connection.queries[-1]))
        project.save()

        return str_project_id

    # ==============================================================================
    #  Insert Subject
    # ==============================================================================
    @staticmethod
    def insert_subject(dic_subject):

        subject = Subject(project_id=dic_subject['projectId'],
                          raw_id=dic_subject['rawId'],
                          subject_nm=dic_subject['subjectNm'],
                          reg_id=dic_subject['regId'],
                          reg_date=dic_subject['regDate'])
        dbLogger.debug("\n{}".format(connection.queries[-1]))
        subject.save()

        return subject.id

    # ==============================================================================
    #  Insert Session
    # ==============================================================================
    @staticmethod
    def insert_session(dic_session):

        session = Session(project_id=dic_session['projectId'],
                          subject_id=dic_session['subjectId'],
                          raw_scan_id=dic_session['rawScanId'],
                          session_nm=dic_session['sessionNm'],
                          reg_id=dic_session['regId'],
                          reg_date=dic_session['regDate'])
        dbLogger.debug("\n{}".format(connection.queries[-1]))
        session.save()

        return session.id

    # ==============================================================================
    #  Insert Scan
    # ==============================================================================
    @staticmethod
    def insert_scan(dic_scan):

        scan = Scan(project_id=dic_scan['projectId'],
                    subject_id=dic_scan['subjectId'],
                    session_id=dic_scan['sessionId'],
                    raw_recon_id=dic_scan['rawReconId'],
                    task=dic_scan['task'],
                    acq=dic_scan['acq'],
                    ce=dic_scan['ce'],
                    rec=dic_scan['rec'],
                    aim=dic_scan['aim'],
                    reg_id=dic_scan['regId'],
                    reg_date=dic_scan['regDate'])
        dbLogger.debug("\n{}".format(connection.queries[-1]))
        scan.save()

        return scan.id

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
        dbLogger.debug("\n{}".format(connection.queries[-1]))

    # ==============================================================================
    #  Update Project
    # ==============================================================================
    @staticmethod
    def update_project_step(project_id, step_code):
        project = ProjectDao.select_project_object(project_id)
        project.step_code = step_code
        project.save()
        dbLogger.debug("\n{}".format(connection.queries[-1]))

    # ==============================================================================
    #  Update Subject
    # ==============================================================================
    @staticmethod
    def update_subject(dic_subject):
        subject = ProjectDao.select_subject_object(dic_subject["subjectId"])
        subject.subject_nm = dic_subject['subjectNm']
        subject.save()
        dbLogger.debug("\n{}".format(connection.queries[-1]))

    # ==============================================================================
    #  Update Session
    # ==============================================================================
    @staticmethod
    def update_session(dic_session):
        session = ProjectDao.select_session_object(dic_session["sessionId"])
        session.session_nm = dic_session['sessionNm']
        session.save()
        dbLogger.debug("\n{}".format(connection.queries[-1]))

    # ==============================================================================
    #  Update Scan
    # ==============================================================================
    @staticmethod
    def update_scan(dic_scan):
        scan = ProjectDao.select_scan_object(dic_scan["scanId"])
        scan.task = dic_scan['task']
        scan.acq = dic_scan['acq']
        scan.ce = dic_scan['ce']
        scan.rec = dic_scan['rec']
        scan.aim = dic_scan['aim']
        scan.save()
        dbLogger.debug("\n{}".format(connection.queries[-1]))

    # ==============================================================================
    #  Delete Scan
    # ==============================================================================
    @staticmethod
    def delete_scan(scan_id):
        scan = ProjectDao.select_scan_object(scan_id)
        scan.delete()

    # ==============================================================================
    #  Delete Session
    # ==============================================================================
    @staticmethod
    def delete_session(session_id):
        session = ProjectDao.select_session_object(session_id)
        session.delete()

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
        query_list.append("          FROM PJO_DB.PJO_CODE     \n")
        query_list.append("         WHERE GROUP_ID = '002'    \n")
        query_list.append("           AND CODE_ID = A.ANIMAL_TYPE) AS ANIMAL_NM \n")
        query_list.append("     , (SELECT CODE_NM             \n")
        query_list.append("          FROM PJO_DB.PJO_CODE     \n")
        query_list.append("         WHERE GROUP_ID = '003'    \n")
        query_list.append("           AND CODE_ID = CONCAT(A.ANIMAL_TYPE, A.STRAIN_TYPE)) AS STRAIN_NM \n")
        query_list.append("     , A.STRAIN_TYPE               \n")
        query_list.append("     , A.CLASSIFICATION            \n")
        query_list.append("     , A.YEAR                      \n")
        query_list.append("     , CONCAT(A.PI_FIRST_NM, ' ', A.PI_LAST_NM) AS RESEARCHER_NM \n")
        query_list.append("     , A.PROJECT_AIM               \n")
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
                result_list = DBUtil().f_dict_fetchall(c)
                dbLogger.debug(''.join(query_list))
            finally:
                c.close()
        return result_list

    # ==============================================================================
    #  Select Project
    # ==============================================================================
    @staticmethod
    def select_project_info(project_id):

        if project_id == "":
            raise Exception("Project ID is missing.")

        # parameter list
        param_list = list()

        # make query
        query_list = list()

        query_list.append("SELECT A.PROJECT_ID                                   \n")
        query_list.append("     , A.INITIAL_NM                                   \n")
        query_list.append("     , CONCAT(A.PI_FIRST_NM, ' ', A.PI_LAST_NM) AS RESEARCHER \n")
        query_list.append("     , A.ANIMAL_TYPE                                  \n")
        query_list.append("     , (SELECT CODE_NM                                \n")
        query_list.append("          FROM PJO_DB.PJO_CODE                        \n")
        query_list.append("         WHERE GROUP_ID = '002'                       \n")
        query_list.append("           AND CODE_ID  = A.ANIMAL_TYPE) AS ANIMAL    \n")
        query_list.append("     , A.STRAIN_TYPE                                  \n")
        query_list.append("     , (SELECT CODE_NM                                \n")
        query_list.append("          FROM PJO_DB.PJO_CODE                        \n")
        query_list.append("         WHERE GROUP_ID = '003'                       \n")
        query_list.append("           AND CODE_ID  = CONCAT(A.ANIMAL_TYPE, A.STRAIN_TYPE)) AS STRAIN \n")
        query_list.append("     , A.CLASSIFICATION                               \n")
        query_list.append("     , A.YEAR                                         \n")
        query_list.append("     , A.PROJECT_AIM                                  \n")
        query_list.append("     , A.STEP_CODE                                    \n")
        query_list.append("  FROM PJO_DB.PJO_PROJECT A                           \n")
        query_list.append(" WHERE A.PROJECT_ID = %s                              \n")

        # param
        param_list.append(project_id)

        # get data
        with connection.cursor() as c:
            try:
                dbLogger.debug(''.join(query_list))
                c.execute(''.join(query_list), param_list)
                dict_result = DBUtil().f_dict_fetchone(c)
            finally:
                c.close()

        if dict_result is None:
            raise Exception("Project does not exist. project_id={}".format(project_id))

        return dict_result

    # ==============================================================================
    #  Select Subject & Raw
    # ==============================================================================
    @staticmethod
    def select_subject_raw(project_id):

        # parameter list
        param_list = list()

        # make query
        query_list = list()

        query_list.append("SELECT A.ID, A.RAW_FOLDER_NM, A.RAW_SAVE_DATE         \n")
        query_list.append("     , A.RAW_RESEARCHER, A.RAW_SPECIMEN, A.RAW_GENDER \n")
        query_list.append("     , A.RAW_AGE, A.RAW_WEIGHT, A.RAW_DELIVERY_DATE   \n")
        query_list.append("     , B.ID AS SUBJECT_ID, B.SUBJECT_NM               \n")
        query_list.append("     , (SELECT COUNT(*) FROM PJO_DB.PJO_RAWSCAN WHERE RAW_ID = A.ID) AS CNT \n")
        query_list.append("  FROM PJO_DB.PJO_RAW A, PJO_DB.PJO_SUBJECT B         \n")
        query_list.append(" WHERE A.ID = B.RAW_ID                                \n")
        query_list.append("   AND B.PROJECT_ID = %s                              \n")
        query_list.append(" ORDER BY A.ID                                        \n")

        # param
        param_list.append(project_id)

        # get data
        with connection.cursor() as c:
            try:
                c.execute(''.join(query_list), param_list)
                result_list = DBUtil().f_dict_fetchall(c)
                dbLogger.debug(''.join(query_list))
            finally:
                c.close()
        return result_list

    # ==============================================================================
    #  Select Scans
    # ==============================================================================
    @staticmethod
    def select_scan_list(raw_id):

        # parameter list
        param_list = list()

        # make query
        query_list = list()

        query_list.append("SELECT A.RAW_ID                                \n")
        query_list.append("     , A.ID  AS RAW_SCAN_ID                    \n")
        query_list.append("     , A.SCAN_NUM                              \n")
        query_list.append("     , A.METHOD                                \n")
        query_list.append("     , A.TE, A.TR, A.BAND_WIDTH, A.FLIP_ANGLE  \n")
        query_list.append("     , CASE WHEN A.FID = 'Y' THEN 'Complete'   \n")
        query_list.append("            WHEN A.FID = 'N' THEN 'Interrupt'  \n")
        query_list.append("       END AS FID                              \n")
        query_list.append("     , IFNULL(B.ID, '') RAW_RECON_ID           \n")
        query_list.append("     , IFNULL(B.RECON_NUM, '') RECON_NO        \n")
        query_list.append("     , IFNULL(B.FOV, '') FOV                   \n")
        query_list.append("     , IFNULL(B.MATRIX, '') MATRIX             \n")
        query_list.append("     , IFNULL(B.RESOLUTION, '') RESOLUTION     \n")
        query_list.append("     , IFNULL(B.THICKNESS, '') THICKNESS       \n")
        query_list.append("     , IFNULL(B.BYTE_ORDER, '') BYTE_ORDER     \n")
        query_list.append("     , IFNULL(B.WORD_TYPE, '') WORD_TYPE       \n")
        query_list.append("     , IFNULL(C.ID, '') SESSION_ID             \n")
        query_list.append("     , IFNULL(C.SESSION_NM, '') SESSION_NM     \n")
        query_list.append("     , IFNULL(D.ID, '') SCAN_ID                \n")
        query_list.append("     , IFNULL(D.TASK, '') TASK                 \n")
        query_list.append("     , IFNULL(D.ACQ, '') ACQ                   \n")
        query_list.append("     , IFNULL(D.CE, '') CE                     \n")
        query_list.append("     , IFNULL(D.REC, '') REC                   \n")
        query_list.append("     , IFNULL(D.RUN, '') RUN                   \n")
        query_list.append("     , IFNULL(D.AIM, '') AIM                   \n")
        query_list.append("  FROM PJO_DB.PJO_RAWSCAN A                    \n")
        query_list.append("  LEFT OUTER JOIN PJO_DB.PJO_RAWRECON B        \n")
        query_list.append("    ON A.ID = B.RAW_SCAN_ID                    \n")
        query_list.append("  LEFT OUTER JOIN PJO_DB.PJO_SESSION C         \n")
        query_list.append("    ON A.ID = C.RAW_SCAN_ID                     \n")
        query_list.append("  LEFT OUTER JOIN PJO_DB.PJO_SCAN D            \n")
        query_list.append("    ON B.ID = D.RAW_RECON_ID                    \n")
        query_list.append(" WHERE A.RAW_ID = %s                           \n")
        query_list.append(" ORDER BY A.ID ASC                             \n")

        # param
        param_list.append(raw_id)

        # get data
        with connection.cursor() as c:
            try:
                c.execute(''.join(query_list), param_list)
                result_list = DBUtil().f_dict_fetchall(c)
                dbLogger.debug(''.join(query_list))
            finally:
                c.close()
        return result_list


