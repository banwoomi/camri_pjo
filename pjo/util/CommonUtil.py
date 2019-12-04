import logging
import os
import shutil
# from datetime import datetime
from django.utils import timezone
from django.utils import dateformat
from django.contrib import messages

logger = logging.getLogger("devLog")
errLogger = logging.getLogger("errLog")


class CommonUtil(object):

    # ==============================================================================
    #  Constructor
    # ==============================================================================
    def __init__(self):
        # do nothing
        pass

    # ==============================================================================
    #  session setting
    # ==============================================================================
    @staticmethod
    def set_session(request, researcher_obj):

        request.session['member_id'] = researcher_obj.id
        request.session['first_name'] = researcher_obj.first_nm
        request.session['last_nm'] = researcher_obj.last_nm
        request.session['authority'] = researcher_obj.authority
        # request.session['last_touch'] = datetime.now()

    # ==============================================================================
    #  session delete
    # ==============================================================================
    @staticmethod
    def del_session(request):

        member_id = request.session.get("member_id")
        if member_id is not None:
            del request.session['member_id']

        first_name = request.session.get("first_name")
        if first_name is not None:
            del request.session['first_name']

        last_nm = request.session.get("last_nm")
        if last_nm is not None:
            del request.session['last_nm']

        authority = request.session.get("authority")
        if authority is not None:
            del request.session['authority']

        last_touch = request.session.get("last_touch")
        if last_touch is not None:
            del request.session['last_touch']

    # ==============================================================================
    #  Get Time Info
    # ==============================================================================
    @staticmethod
    def f_get_date_time():
        return timezone.now()

    # ==============================================================================
    #  Get Date Info
    #     = Y:year
    #     = M:month
    #     = D:day
    # ==============================================================================
    @staticmethod
    def f_get_date(d_type):

        # result
        date = ""

        if d_type == "Y":
            date = CommonUtil.f_get_date_time().year
        elif d_type == "M":
            date = CommonUtil.f_get_date_time().month
        elif d_type == "D":
            date = CommonUtil.f_get_date_time().day

        return date

    # ==============================================================================
    #  Get Time Using Format
    #  format : https://docs.djangoproject.com/en/1.10/ref/templates/builtins/#date
    #    ex) Y-m-d H:i ==> 2016-01-12 23:20
    #        y-M-D h:i ==> 16-Jan-Fri 11:20
    # ==============================================================================
    @staticmethod
    def f_get_date_time_format(str_format):
        return dateformat.format(CommonUtil().f_get_date_time(), str_format)

    # ==============================================================================
    #  Get Message Tags
    # ==============================================================================
    @staticmethod
    def f_get_message_tag(int_msg):

        switcher = {
            10: 'debug',
            20: 'info',
            25: 'success',
            30: 'warning',
            40: 'error'
        }
        return switcher.get(int_msg, 'INFO')




