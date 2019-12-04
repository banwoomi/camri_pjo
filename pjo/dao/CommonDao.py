import logging
from django.shortcuts import get_object_or_404
from django.db.models import Count
from pjo.models import Code
from pjo.models import CodeGroup

dbLogger = logging.getLogger("dba")
errLogger = logging.getLogger("errLog")


class CommonDao(object):

    # ==============================================================================
    #  Select Common Code
    # ==============================================================================
    @staticmethod
    def select_code_list(group_id):
        code_list = Code.objects.filter(group_id=group_id).values().order_by('order_no')

        return code_list

    # ==============================================================================
    #  Select Common Code for Json
    # ==============================================================================
    @staticmethod
    def select_code_list_for_json(group_id):
        code_list = Code.objects.filter(group_id=group_id).only('code_id', 'code_nm').order_by('order_no')

        return code_list

    # ==============================================================================
    #  Select Common Code Value
    # ==============================================================================
    @staticmethod
    def select_code_object(group_id, code_id):
        code = get_object_or_404(Code, group_id=group_id, code_id=code_id)

        return code



