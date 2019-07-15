import json
import logging
import os
from django.shortcuts import render
from django.http import HttpResponse

from pjo.dao.MemberDao import MemberDao

logger = logging.getLogger("devLog")
dbLogger = logging.getLogger("dba")
errLogger = logging.getLogger("errLog")


# ==============================================================================
#  index page
# ==============================================================================
def cam_main(request):

    template_name = 'pjo_main.html'

    context = {
    }

    return render(request, template_name, context)



'''
##########################################################################################################
#  [Sign in] JOIN as a member
##########################################################################################################
'''


# ==============================================================================
#  Sign Up Form page
# ==============================================================================
def sign_up_form(request):

    template_name = 'member/sign_up.html'
    context = {
        'title': 'Sign Up',
    }

    return render(request, template_name, context)


# ==============================================================================
#  check duplication before join
# ==============================================================================
def check_id(request):

    str_value = request.POST['userId']
    logger.debug("ID : [" + str_value + "]")

    researcher = MemberDao.select_researcher_for_check(str_value)
    r_count = researcher.count()


    json_str = json.dumps(r_count)
    return HttpResponse(json_str, content_type='application/json')

