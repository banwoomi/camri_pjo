import json
import logging
import os
import re
import datetime

from django.contrib import messages
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect

from pjo.dao.MemberDao import MemberDao
from pjo.dao.CommonDao import CommonDao
from pjo.dao.ProjectDao import ProjectDao
from pjo.util.CommonUtil import CommonUtil
from pjo.util.PjoException import PjoException
from pjo.util.Properties import Properties

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

    # messages.debug(request, 'Total records updated {0}'.format(1))
    # messages.info(request, 'Improve your profile today!')
    # messages.success(request, 'Your password was updated successfully!')
    # messages.warning(request, 'Please correct the error below.')
    # messages.error(request, 'An unexpected error occured.')
    return render(request, template_name, context)


'''
##########################################################################################################
#  [Common]
##########################################################################################################
'''


# ==============================================================================
#  Select Code
# ==============================================================================
def common_code_inq(request):

    if 'txtCodeId' in request.POST:
        code_id = request.POST['txtCodeId']
    else:
        code_id = ""
    logger.debug("ID : [" + code_id + "]")

    list_code = CommonDao.select_code_list_for_json(code_id)
    json_result = serializers.serialize("json", list_code)

    # list_code = CommonDao.select_code_list(code_id)
    logger.debug(json_result)

    # json_str = json.dumps(list_code)
    return HttpResponse(json_result, content_type='application/json')
    # return HttpResponse(json_str, content_type='application/json')
    # return JsonResponse(list_code)


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

    researcher = MemberDao.select_researcher_for_check("ID", str_value)
    r_count = researcher.count()

    json_str = json.dumps(r_count)

    return HttpResponse(json_str, content_type='application/json')


# ==============================================================================
#  Sign Up as member : [INSERT RESEARCHER]
# ==============================================================================
def sign_up(request):

    # Values
    sign_id = request.POST['txtId']
    logger.debug("Sign Up ID [" + sign_id + "]")

    # Return
    dic_return = dict()

    # Set Dictionary
    dic_researcher = dict()

    dic_researcher['id'] = sign_id
    dic_researcher['firstName'] = request.POST['txtFirstName']
    dic_researcher['lastName'] = request.POST['txtLastName']
    dic_researcher['password'] = request.POST['txtPassword']
    dic_researcher['regDate'] = CommonUtil.f_get_date_time()

    try:
        # Insert
        result = MemberDao.insert_researcher(dic_researcher)

        if result:
            dic_return['ret_code'] = "Y"
            dic_return['ret_level'] = CommonUtil.f_get_message_tag(messages.SUCCESS)
            dic_return['ret_msg'] = "Join Success!! Please Sign in!!"
        else:
            dic_return['ret_code'] = "N"
            dic_return['ret_level'] = CommonUtil.f_get_message_tag(messages.WARNING)
            dic_return['ret_msg'] = "ID already exists."

    except Exception as e:
        r = PjoException(exception=e, user_msg="Failed to register.", user_id=request.session.get("member_id"))
        r.process()
        dic_return['ret_code'] = "N"
        dic_return['ret_level'] = CommonUtil.f_get_message_tag(messages.WARNING)
        dic_return['ret_msg'] = r.message

    return JsonResponse(dic_return)


# ==============================================================================
#  Sign In Form page
# ==============================================================================
def sign_form(request):

    template_name = 'member/sign_in.html'
    context = {
        'title': 'Sign In',
    }

    return render(request, template_name, context)


# ==============================================================================
#  Sign In
# ==============================================================================
def sign_in(request):

    # Values
    str_id = request.POST['txtId']
    str_password = request.POST['txtPassword']
    logger.debug("Sign In ID [" + str_id + "]")

    # Return
    dic_return = dict()

    # Set Dictionary
    dic_researcher = dict()
    dic_researcher['id'] = str_id
    dic_researcher['password'] = str_password

    # check ID
    researcher = MemberDao.select_researcher_for_check("ID", str_id)

    if researcher.count() == 0:
        dic_return['ret_code'] = "A"
        dic_return['ret_msg'] = "Incorrect ID. Please try again."
    else:
        # check ID & Password
        if researcher[0].password == str_password:
            obj_researcher = researcher[0]

            # session setting
            CommonUtil.set_session(request, obj_researcher)

            dic_return['ret_code'] = "Y"

        else:

            dic_return['ret_code'] = "B"
            dic_return['ret_msg'] = "Incorrect Password. Please try again."

            # delete session
            CommonUtil.del_session(request)
            logger.debug("errMsg: [" + dic_return['ret_msg'] + "]")

    return JsonResponse(dic_return)


# ==============================================================================
#  Sign out
# ==============================================================================
def sign_out(request):

    template_name = 'pjo_main.html'
    context = {
    }

    # session delete
    CommonUtil.del_session(request)

    return render(request, template_name, context)


# ==============================================================================
#  Profile Form
# ==============================================================================
def profile_form(request):

    template_name = 'member/profile.html'
    context = {
        'title': 'My Profile',
    }

    # values
    sign_id = request.session['member_id']
    logger.debug("signId [" + sign_id + "]")

    # get common code
    code001 = CommonDao.select_code_list("001")

    # Dao
    researcher = MemberDao.select_researcher_object(sign_id)
    logger.debug(researcher.reg_date)

    # setting context
    context['id'] = researcher.id
    context['firstName'] = researcher.first_nm
    context['lastName'] = researcher.last_nm
    context['password'] = researcher.password
    context['authority'] = researcher.authority
    context['code001'] = code001

    return render(request, template_name, context)


# ==============================================================================
#  Modify Profile
# ==============================================================================
def profile_modify(request):

    # Return
    dic_return = dict()

    # Set Dictionary
    dic_researcher = dict()
    dic_researcher['id'] = request.POST['txtId']
    dic_researcher['firstName'] = request.POST['txtFirstName']
    dic_researcher['lastName'] = request.POST['txtLastName']
    dic_researcher['password'] = request.POST['txtPassword']
    dic_researcher['authority'] = request.POST['selAuthority']
    logger.debug("Sign In ID [" + dic_researcher['id'] + "]")

    try:
        # Update
        MemberDao.update_researcher(dic_researcher)

        dic_return['ret_code'] = "Y"
        dic_return['ret_level'] = CommonUtil.f_get_message_tag(messages.SUCCESS)
        dic_return['ret_msg'] = "You have successfully modified your account!"

    except Exception as e:
        r = PjoException(exception=e, user_msg="Failed to change profile.", user_id=request.session.get("member_id"))
        r.process()
        dic_return['ret_code'] = "N"
        dic_return['ret_level'] = CommonUtil.f_get_message_tag(messages.WARNING)
        dic_return['ret_msg'] = r.message

    return JsonResponse(dic_return)


# ==============================================================================
#  Project Form
# ==============================================================================
def project_form(request):

    template_name = 'project/project.html'
    context = {
        'title': 'Register Project',
    }

    if 'signYn' in context:
        template_name = 'member/sign_in.html'
    else:

        # values
        reg_id = request.session['member_id']
        logger.debug("reg_id [" + reg_id + "]")

        # get common code
        code002 = CommonDao.select_code_list("002")
        code004 = CommonDao.select_code_list("004")

        context['code002'] = code002
        context['code004'] = code004

    return render(request, template_name, context)


# ==============================================================================
#  Project Modify
# ==============================================================================
def project_modify(request, project_id):

    template_name = 'project/project.html'
    context = {
        'title': 'Modify Project',
    }

    if 'signYn' in context:
        template_name = 'member/sign_in.html'
    else:

        # values
        logger.debug("project_id [" + project_id + "]")
        reg_id = request.session['member_id']
        logger.debug("reg_id [" + reg_id + "]")

        # get common code
        code002 = CommonDao.select_code_list("002")
        code004 = CommonDao.select_code_list("004")

        # Dao
        if project_id:
            project = ProjectDao.select_project_object(project_id)

            # setting context
            context['project_id'] = project_id
            context['firstName'] = project.pi_first_nm
            context['lastName'] = project.pi_last_nm
            context['piInitial'] = project.initial_nm
            context['animalType'] = project.animal_type
            context['strainType'] = project.strain_type
            context['classification'] = project.classification
            context['year'] = project.year[2:4]
            context['projectAim'] = project.project_aim

        context['code002'] = code002
        context['code004'] = code004

    return render(request, template_name, context)


# ==============================================================================
#  Project Register
# ==============================================================================
def project_register(request):

    template_name = 'project/project.html'
    context = {
        'title': 'Project Detail',
    }

    if 'signYn' in context:
        template_name = 'member/sign_in.html'
    else:

        mod_project_id = request.POST['txtProjectId']
        logger.debug("## mod_project_id=={}".format(mod_project_id))

        # Return
        dic_result = dict()

        try:
            if mod_project_id == "":

                # Set Dictionary
                dic_project = dict()
                dic_project['firstName'] = request.POST['txtFirstName']
                dic_project['lastName'] = request.POST['txtLastName']
                dic_project['piInit'] = request.POST['txtPIInit']
                dic_project['animalType'] = request.POST['selAnimalType']
                dic_project['animalStrain'] = request.POST['selAnimalStrain']
                dic_project['classification'] = request.POST['txtClassification']
                dic_project['year'] = request.POST['selYear']
                dic_project['projectAim'] = request.POST['txtProjectAim']
                dic_project['regId'] = request.session.get("member_id")
                dic_project['regDate'] = CommonUtil.f_get_date_time()

                # Insert
                project_id = ProjectDao.insert_project(dic_project)

                dic_result['projectId'] = project_id
                dic_result['ret_code'] = "I"
                dic_result['ret_level'] = CommonUtil.f_get_message_tag(messages.SUCCESS)
                dic_result['ret_msg'] = "Project Registration success."

            else:
                # Set Dictionary
                dic_project = dict()
                dic_project['projectId'] = mod_project_id
                dic_project['firstName'] = request.POST['txtFirstName']
                dic_project['lastName'] = request.POST['txtLastName']
                dic_project['year'] = request.POST['selYear']
                dic_project['projectAim'] = request.POST['txtProjectAim']

                # Update
                ProjectDao.update_project(dic_project)

                dic_result['projectId'] = mod_project_id
                dic_result['ret_code'] = "U"
                dic_result['ret_level'] = CommonUtil.f_get_message_tag(messages.SUCCESS)
                dic_result['ret_msg'] = "Project Modification success."

        except Exception as e:
            r = PjoException(exception=e, user_msg="Failed to register.", user_id=request.session.get("member_id"))
            r.process()
            dic_result['ret_code'] = "F"
            dic_result['ret_level'] = CommonUtil.f_get_message_tag(messages.WARNING)
            dic_result['ret_msg'] = r.message

        return JsonResponse(dic_result)


# ==============================================================================
#  Project List
# ==============================================================================
def project_search(request):

    template_name = 'project/project_list.html'
    context = {
        'title': 'Search Project',
    }

    if 'signYn' in context:
        template_name = 'member/sign_in.html'
    else:

        # ---------------------------------------------------------------------
        #  get default items
        # ---------------------------------------------------------------------
        # get common code
        code002 = CommonDao.select_code_list("002")
        code004 = CommonDao.select_code_list("004")

        # setting context
        context['code002'] = code002
        context['code004'] = code004

        # ---------------------------------------------------------------------
        #  get project list
        # ---------------------------------------------------------------------
        #  get parameters
        if 'txtPIInit' in request.POST:
            str_pi_initial = request.POST['txtPIInit']
            print(str_pi_initial)
            context['txtPIInit'] = str_pi_initial

        if 'txtPIName' in request.POST:
            str_pi_name = request.POST['txtPIName']
            context['txtPIName'] = str_pi_name

        if 'selAnimalType' in request.POST:
            str_animal_type = request.POST['selAnimalType']
            context['selAnimalType'] = str_animal_type

        if 'selYear' in request.POST:
            str_year = request.POST['selYear']
            context['selYear'] = str_year

        if 'txtProjectAim' in request.POST:
            str_project_aim = request.POST['txtProjectAim']
            context['txtProjectAim'] = str_project_aim

        if 'txtPage' in request.POST:
            str_page = request.POST['txtPage']
            context['txtPage'] = str_page
        else:
            str_page = 1

        try:

            # Get Project List
            result_list = ProjectDao.select_project_list(context)

            # Paginator
            paginator = Paginator(result_list, 20)

            try:
                result_list = paginator.page(str_page)
            except PageNotAnInteger:
                result_list = paginator.page(1)
            except EmptyPage:
                result_list = paginator.page(paginator.num_pages)

            # context setting
            context['resultList'] = result_list

        except Exception as e:
            r = PjoException(exception=e, user_msg="Failed to search project list.",
                             user_id=request.session.get("member_id"))
            r.process()
            messages.error(request, "Error occurred while searching the Project list")

        return render(request, template_name, context)


# ==============================================================================
#  Raw Form
# ==============================================================================
def raw_form(request):

    template_name = 'project/raw_list.html'
    context = {
        'title': 'Raw Files',
    }

    if 'signYn' in context:
        template_name = 'member/sign_in.html'
    else:

        # values
        reg_id = request.session['member_id']
        logger.debug("reg_id [" + reg_id + "]")

    return render(request, template_name, context)


# ==============================================================================
#  Register Raw
# ==============================================================================
def raw_register(request):

    template_name = 'project/raw_list.html'
    context = {
        'title': 'Raw Files',
    }

    if 'signYn' in context:
        template_name = 'member/sign_in.html'
    else:
        path_raw = Properties.path_raw()
        logger.debug("path_raw==[{}]".format(path_raw))

        # values
        dic_raw = dict()
        dic_raw['regId'] = request.session.get("member_id")
        dic_raw['regDate'] = CommonUtil.f_get_date_time()

        # Return
        dic_result = dict()

        try:
            # Make a file list from the directory
            if not os.path.isdir(path_raw):
                raise Exception("Path does not exist. path=[" + path_raw + "]")

            list_raw = os.listdir(path_raw)
            num_insert = 0
            for raw_file in list_raw:
                file_nm = re.split(".zip", raw_file)
                if len(file_nm) > 1:

                    # Check DB
                    list_raw = ProjectDao.select_raw_list_by_name(file_nm[0])
                    len_raw = len(list_raw)
                    logger.debug("# {}=len:[{}]".format(file_nm[0], len_raw))

                    if len_raw == 0:
                        # Insert DB
                        save_time = os.path.getmtime(os.path.join(path_raw, raw_file))
                        save_time = datetime.datetime.fromtimestamp(save_time)
                        save_time = save_time.strftime('%Y%m%d')
                        dic_raw['rawFolderNm'] = file_nm[0]
                        dic_raw['rawSaveDate'] = save_time
                        ProjectDao.insert_raw(dic_raw)
                        num_insert = num_insert + 1

            if num_insert == 0:
                dic_result['ret_code'] = "I"
                dic_result['ret_level'] = CommonUtil.f_get_message_tag(messages.DEBUG)
                dic_result['ret_msg'] = "There is no raw folder to save."
            else:
                dic_result['ret_code'] = "I"
                dic_result['ret_level'] = CommonUtil.f_get_message_tag(messages.SUCCESS)
                dic_result['ret_msg'] = "Raw Registration success. [Success:" + str(num_insert) + "]"

        except Exception as e:
            r = PjoException(exception=e, user_msg="Failed to register raw.", user_id=request.session.get("member_id"))
            r.process()
            dic_result['ret_code'] = "F"
            dic_result['ret_level'] = CommonUtil.f_get_message_tag(messages.WARNING)
            dic_result['ret_msg'] = r.message

        return JsonResponse(dic_result)


# ==============================================================================
#  Raw List
# ==============================================================================
def raw_search(request):

    template_name = 'project/raw_list.html'
    context = {
        'title': 'Raw Files',
    }

    if 'signYn' in context:
        template_name = 'member/sign_in.html'
    else:

        # ---------------------------------------------------------------------
        #  get project list
        # ---------------------------------------------------------------------
        #  get parameters
        if 'txtRawFileNm' in request.POST:
            str_raw_file = request.POST['txtRawFileNm']
            context['txtRawFileNm'] = str_raw_file

        if 'txtStartScanDate' in request.POST:
            str_start_date = request.POST['txtStartScanDate']
            context['txtStartScanDate'] = str_start_date
            if str_start_date != "":
                arr_start_date = str_start_date.split("/")
                context['txtStartDate'] = arr_start_date[2] + arr_start_date[0] + arr_start_date[1]

        if 'txtEndScanDate' in request.POST:
            str_end_date = request.POST['txtEndScanDate']
            context['txtEndScanDate'] = str_end_date
            if str_end_date != "":
                arr_end_date = str_end_date.split("/")
                context['txtEndDate'] = arr_end_date[2] + arr_end_date[0] + arr_end_date[1]

        if 'selConvertYn' in request.POST:
            str_convert = request.POST['selConvertYn']
            context['selConvertYn'] = str_convert

        if 'selBackupYn' in request.POST:
            str_backup = request.POST['selBackupYn']
            context['selBackupYn'] = str_backup

        if 'txtPage' in request.POST:
            str_page = request.POST['txtPage']
            context['txtPage'] = str_page
        else:
            str_page = 1

        try:

            # Get Raw List
            result_list = ProjectDao.select_raw_list(context)

            # Paginator
            paginator = Paginator(result_list, 20)

            try:
                result_list = paginator.page(str_page)
            except PageNotAnInteger:
                result_list = paginator.page(1)
            except EmptyPage:
                result_list = paginator.page(paginator.num_pages)

            # context setting
            context['resultList'] = result_list

        except Exception as e:
            r = PjoException(exception=e, user_msg="Failed to search raw list.",
                             user_id=request.session.get("member_id"))
            r.process()
            messages.error(request, "Error occurred while searching the Raw list")

        return render(request, template_name, context)





