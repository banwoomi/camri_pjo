import logging
from django.db import connection
from django.shortcuts import get_object_or_404
from pjo.models import Researcher

dbLogger = logging.getLogger("dba")
errLogger = logging.getLogger("errLog")


class MemberDao(object):

    def __init__(self):
        pass

    """
    ==============================================================================
     Researcher
    ==============================================================================
    """

    # ==============================================================================
    #  Select Researcher Object
    # ==============================================================================
    @staticmethod
    def select_researcher_object(join_id):

        researcher = get_object_or_404(Researcher, pk=join_id)

        return researcher

    # ==============================================================================
    #  Select Researcher
    # ==============================================================================
    @staticmethod
    def select_researcher_for_check(flag, str_value):

        # Check Initial
        if flag == 'Initial':
            researcher = Researcher.objects.filter(initial_nm=str_value)

        # Check ID
        elif flag == 'ID':
            researcher = Researcher.objects.filter(id=str_value)

        # Other
        else:
            researcher = None

        return researcher

    # ==============================================================================
    #  Insert Researcher
    # ==============================================================================
    @staticmethod
    def insert_researcher(dic_researcher):

        # Duplicate check
        researcher = Researcher.objects.filter(pk=dic_researcher['id'])

        if researcher.count() == 0:
            researcher = Researcher(id=dic_researcher['id'],
                                    first_nm=dic_researcher['firstName'],
                                    last_nm=dic_researcher['lastName'],
                                    password=dic_researcher['password'],
                                    reg_date=dic_researcher['regDate'])
            researcher.save()
            dbLogger.debug(connection.queries[-1])
            return True
        else:
            errLogger.error("Already Exists. ID=[" + dic_researcher['id'] + "]")
            return False

    # ==============================================================================
    #  Update Researcher
    # ==============================================================================
    @staticmethod
    def update_researcher(dic_researcher):

        # UPDATE
        researcher = MemberDao.select_researcher_object(dic_researcher['id'])
        researcher.first_nm = dic_researcher['firstName']
        researcher.last_nm = dic_researcher['lastName']
        researcher.password = dic_researcher['password']
        researcher.authority = dic_researcher['authority']
        researcher.save()
        dbLogger.debug(connection.queries[-1])


