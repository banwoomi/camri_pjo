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

from pjo.module.BrukerIOConverter import Study, Scan, Recon

from pjo.dao.MemberDao import MemberDao
from pjo.dao.CommonDao import CommonDao
from pjo.dao.ProjectDao import ProjectDao
from pjo.dao.RawDao import RawDao

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

    template_name = "pjo_main.html"
    context = {
    }

    try:
        logger.debug("Hello World!!")



        # try:
    #     # path_study = "/Users/woomi_mac/Downloads/PJO_test/step1_rawfiles_zip/20191124_152008_MM191124_1_1"
    #     # path_study = "/Users/woomi_mac/Downloads/PJO_test/step1_rawfiles_zip/20191124_152008_MM191124_1_1.zip"
    #     # path_study = "/Users/woomi_mac/Downloads/PJO_test/step1_rawfiles_zip/20191113_094659_earfilling_toothpate_test_1_1"
    #     path_study = "/Users/woomi_mac/Downloads/PJO_test/step1_rawfiles_zip/fftest.zip"
    #
    #     #-----------------------
    #     # Study
    #     study_obj = Study(path_study, log_handler=logger)
    #     list_scan = study_obj.scan_list
    #     logger.debug("list_scan==[{}]".format(list_scan))
    #
    #     #-----------------------
    #     # Scan
    #     scan_no = list_scan[-1]
    #     # scan_no = 31
    #     # scan_no = 36
    #     scan_obj = study_obj.get_scan(scan_no)
    #
    #     list_recon = scan_obj.recon_list
    #
    #     #-----------------------
    #     # Recon
    #     recon_no = list_recon[0]
    #     recon_obj = scan_obj.get_recon(recon_no)
    #     recon_obj.get_param()
    #     print("######################## 1")
    #     print(recon_obj.path_study)
    #     print("######################## 2")
    #
    #     #-----------------------
    #     # Conversion
    #     conv_obj = recon_obj.get_conversion()
    #     path_save = os.path.join(Properties.path_brkraw(), recon_obj.recon_var["path_save"])
    #     conv_obj.save(path_save, recon_obj.recon_var["file_nm"])
    #
    # except Exception as e:
    #     r = PjoException(exception=e, user_msg="####", user_id=request.session.get("member_id"))
    #     r.process()

    # messages.debug(request, "Total records updated {0}".format(1))
    # messages.info(request, "Improve your profile today!")
    # messages.success(request, "Your password was updated successfully!")
    # messages.warning(request, "Please correct the error below.")
    # messages.error(request, "An unexpected error occured.")

    except Exception as e:
        r = PjoException(exception=e, user_msg="[cam_main] Error occurred.",
                         user_id=request.session.get("member_id"))
        r.process()
        messages.error(request, r.message)

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

    try:
        if "txtCodeId" in request.POST:
            code_id = request.POST["txtCodeId"]
        else:
            code_id = ""
        logger.debug("ID : [" + code_id + "]")

        list_code = CommonDao.select_code_list_for_json(code_id)
        json_result = serializers.serialize("json", list_code)

        # list_code = CommonDao.select_code_list(code_id)
        logger.debug(json_result)

    except Exception as e:
        r = PjoException(exception=e, user_msg="[common_code_inq] Error occurred.",
                         user_id=request.session.get("member_id"))
        r.process()
        messages.error(request, r.message)

    return HttpResponse(json_result, content_type="application/json")


'''
##########################################################################################################
#  [Sign in] JOIN as a member
##########################################################################################################
'''


# ==============================================================================
#  Sign Up Form page
# ==============================================================================
def sign_up_form(request):

    template_name = "member/sign_up.html"
    context = {
        "title": "Sign Up",
    }

    return render(request, template_name, context)


# ==============================================================================
#  check duplication before join
# ==============================================================================
def check_id(request):

    str_value = request.POST["userId"]
    logger.debug("ID : [" + str_value + "]")

    researcher = MemberDao.select_researcher_for_check("ID", str_value)
    r_count = researcher.count()

    json_str = json.dumps(r_count)

    return HttpResponse(json_str, content_type="application/json")


# ==============================================================================
#  Sign Up as member : [INSERT RESEARCHER]
# ==============================================================================
def sign_up(request):

    try:

        # Values
        sign_id = request.POST["txtId"]
        logger.debug("Sign Up ID [" + sign_id + "]")

        # Return
        dic_return = dict()

        # Set Dictionary
        dic_researcher = dict()

        dic_researcher["id"] = sign_id
        dic_researcher["firstName"] = request.POST["txtFirstName"]
        dic_researcher["lastName"] = request.POST["txtLastName"]
        dic_researcher["password"] = request.POST["txtPassword"]
        dic_researcher["regDate"] = CommonUtil.f_get_date_time()

        # Insert
        result = MemberDao.insert_researcher(dic_researcher)

        if result:
            dic_return["ret_code"] = "Y"
            dic_return["ret_level"] = CommonUtil.f_get_message_tag(messages.SUCCESS)
            dic_return["ret_msg"] = "Join Success!! Please Sign in!!"
        else:
            dic_return["ret_code"] = "N"
            dic_return["ret_level"] = CommonUtil.f_get_message_tag(messages.WARNING)
            dic_return["ret_msg"] = "ID already exists."

    except Exception as e:
        r = PjoException(exception=e, user_msg="[sign_up] Error occurred.", user_id=request.session.get("member_id"))
        r.process()
        dic_return["ret_code"] = "N"
        dic_return["ret_level"] = CommonUtil.f_get_message_tag(messages.WARNING)
        dic_return["ret_msg"] = r.message

    return JsonResponse(dic_return)


# ==============================================================================
#  Sign In Form page
# ==============================================================================
def sign_form(request):

    template_name = "member/sign_in.html"
    context = {
        "title": "Sign In",
    }

    return render(request, template_name, context)


# ==============================================================================
#  Sign In
# ==============================================================================
def sign_in(request):

    try:

        # Values
        str_id = request.POST["txtId"]
        str_password = request.POST["txtPassword"]
        logger.debug("Sign In ID [" + str_id + "]")

        # Return
        dic_return = dict()

        # Set Dictionary
        dic_researcher = dict()
        dic_researcher["id"] = str_id
        dic_researcher["password"] = str_password

        # check ID
        researcher = MemberDao.select_researcher_for_check("ID", str_id)

        if researcher.count() == 0:
            dic_return["ret_code"] = "A"
            dic_return["ret_msg"] = "Incorrect ID. Please try again."
        else:
            # check ID & Password
            if researcher[0].password == str_password:
                obj_researcher = researcher[0]

                # session setting
                CommonUtil.set_session(request, obj_researcher)

                dic_return["ret_code"] = "Y"

            else:

                dic_return["ret_code"] = "B"
                dic_return["ret_msg"] = "Incorrect Password. Please try again."

                # delete session
                CommonUtil.del_session(request)
                logger.debug("errMsg: [" + dic_return["ret_msg"] + "]")

    except Exception as e:
        r = PjoException(exception=e, user_msg="[sign_in] Error occurred.", user_id=request.session.get("member_id"))
        r.process()
        dic_return["ret_code"] = "N"
        dic_return["ret_level"] = CommonUtil.f_get_message_tag(messages.WARNING)
        dic_return["ret_msg"] = r.message

    return JsonResponse(dic_return)


# ==============================================================================
#  Sign out
# ==============================================================================
def sign_out(request):

    try:
        template_name = "pjo_main.html"
        context = {
        }

        # session delete
        CommonUtil.del_session(request)

    except Exception as e:
        r = PjoException(exception=e, user_msg="[sign_out] Error occurred.", user_id=request.session.get("member_id"))
        r.process()
        messages.error(request, r.message)

    return render(request, template_name, context)


# ==============================================================================
#  Profile Form
# ==============================================================================
def profile_form(request):

    try:
        template_name = "member/profile.html"
        context = {
            "title": "My Profile",
        }

        # values
        sign_id = request.session["member_id"]
        logger.debug("signId [" + sign_id + "]")

        # get common code
        code001 = CommonDao.select_code_list("001")

        # Dao
        researcher = MemberDao.select_researcher_object(sign_id)
        logger.debug(researcher.reg_date)

        # setting context
        context["id"] = researcher.id
        context["firstName"] = researcher.first_nm
        context["lastName"] = researcher.last_nm
        context["password"] = researcher.password
        context["authority"] = researcher.authority
        context["code001"] = code001

    except Exception as e:
        r = PjoException(exception=e, user_msg="[profile_form] Error occurred.",
                         user_id=request.session.get("member_id"))
        r.process()
        messages.error(request, r.message)

    return render(request, template_name, context)


# ==============================================================================
#  Modify Profile
# ==============================================================================
def profile_modify(request):

    try:
        # Return
        dic_return = dict()

        # Set Dictionary
        dic_researcher = dict()
        dic_researcher["id"] = request.POST["txtId"]
        dic_researcher["firstName"] = request.POST["txtFirstName"]
        dic_researcher["lastName"] = request.POST["txtLastName"]
        dic_researcher["password"] = request.POST["txtPassword"]
        dic_researcher["authority"] = request.POST["selAuthority"]
        logger.debug("Sign In ID [" + dic_researcher["id"] + "]")

        # Update
        MemberDao.update_researcher(dic_researcher)

        dic_return["ret_code"] = "Y"
        dic_return["ret_level"] = CommonUtil.f_get_message_tag(messages.SUCCESS)
        dic_return["ret_msg"] = "You have successfully modified your account!"

    except Exception as e:
        r = PjoException(exception=e, user_msg="[profile_modify] Error occurred.",
                         user_id=request.session.get("member_id"))
        r.process()
        dic_return["ret_code"] = "N"
        dic_return["ret_level"] = CommonUtil.f_get_message_tag(messages.WARNING)
        dic_return["ret_msg"] = r.message

    return JsonResponse(dic_return)


'''
##########################################################################################################
#  [Project] 
##########################################################################################################
'''


# ==============================================================================
#  Project Form
# ==============================================================================
def project_form(request):

    try:
        template_name = "project/project.html"
        context = {
            "title": "Register Project",
        }

        if 'member_id' not in request.session:
            context["title"] = "Sign In"
            template_name = "member/sign_in.html"
        else:

            # values
            reg_id = request.session["member_id"]
            logger.debug("reg_id [" + reg_id + "]")

            # get common code
            code002 = CommonDao.select_code_list("002")
            code004 = CommonDao.select_code_list("004")

            context["code002"] = code002
            context["code004"] = code004

    except Exception as e:
        r = PjoException(exception=e, user_msg="[project_form] Error occurred.",
                         user_id=request.session.get("member_id"))
        r.process()
        messages.error(request, r.message)

    return render(request, template_name, context)


# ==============================================================================
#  Project Register
# ==============================================================================
def project_register(request):

    template_name = "project/project.html"
    context = {
        "title": "Project Detail",
    }

    try:
        if 'member_id' not in request.session:
            context["title"] = "Sign In"
            template_name = "member/sign_in.html"
        else:

            mod_project_id = request.POST["txtProjectId"]
            logger.debug("## mod_project_id=={}".format(mod_project_id))

            # Return
            dic_result = dict()

            if mod_project_id == "":

                # Set Dictionary
                dic_project = dict()
                dic_project["firstName"] = request.POST["txtFirstName"]
                dic_project["lastName"] = request.POST["txtLastName"]
                dic_project["piInit"] = request.POST["txtPIInit"]
                dic_project["animalType"] = request.POST["selAnimalType"]
                dic_project["animalStrain"] = request.POST["selAnimalStrain"]
                dic_project["classification"] = request.POST["txtClassification"]
                dic_project["year"] = "20" + request.POST["selYear"]
                dic_project["projectAim"] = request.POST["txtProjectAim"]
                dic_project["regId"] = request.session.get("member_id")
                dic_project["regDate"] = CommonUtil.f_get_date_time()

                # Insert
                project_id = ProjectDao.insert_project(dic_project)

                dic_result["projectId"] = project_id
                dic_result["ret_code"] = "I"
                dic_result["ret_level"] = CommonUtil.f_get_message_tag(messages.SUCCESS)
                dic_result["ret_msg"] = "Project Registration success."

            else:
                # Set Dictionary
                dic_project = dict()
                dic_project["projectId"] = mod_project_id
                dic_project["firstName"] = request.POST["txtFirstName"]
                dic_project["lastName"] = request.POST["txtLastName"]
                dic_project["year"] = "20" + request.POST["selYear"]
                dic_project["projectAim"] = request.POST["txtProjectAim"]

                # Update
                ProjectDao.update_project(dic_project)

                dic_result["projectId"] = mod_project_id
                dic_result["ret_code"] = "U"
                dic_result["ret_level"] = CommonUtil.f_get_message_tag(messages.SUCCESS)
                dic_result["ret_msg"] = "Project Modification success."

    except Exception as e:
        r = PjoException(exception=e, user_msg="[project_register] Error occurred.",
                         user_id=request.session.get("member_id"))
        r.process()
        dic_result["ret_code"] = "F"
        dic_result["ret_level"] = CommonUtil.f_get_message_tag(messages.WARNING)
        dic_result["ret_msg"] = r.message

    return JsonResponse(dic_result)


# ==============================================================================
#  Project Modify form
# ==============================================================================
def project_modify_frm(request, project_id):

    try:
        template_name = "project/project.html"
        context = {
            "title": "Modify Project",
        }

        if 'member_id' not in request.session:
            context["title"] = "Sign In"
            template_name = "member/sign_in.html"
        else:

            # values
            logger.debug("project_id [" + project_id + "]")

            # get common code
            code002 = CommonDao.select_code_list("002")
            code004 = CommonDao.select_code_list("004")

            # Dao
            if project_id:
                project = ProjectDao.select_project_object(project_id)

                # setting context
                context["project_id"] = project_id
                context["firstName"] = project.pi_first_nm
                context["lastName"] = project.pi_last_nm
                context["piInitial"] = project.initial_nm
                context["animalType"] = project.animal_type
                context["strainType"] = project.strain_type
                context["classification"] = project.classification
                context["year"] = project.year[2:4]
                context["projectAim"] = project.project_aim

            context["code002"] = code002
            context["code004"] = code004

    except Exception as e:
        r = PjoException(exception=e, user_msg="[project_modify_frm] Error occurred.",
                         user_id=request.session.get("member_id"))
        r.process()
        messages.error(request, r.message)

    return render(request, template_name, context)


# ==============================================================================
#  Project List
# ==============================================================================
def project_search(request):

    try:

        template_name = "project/project_list.html"
        context = {
            "title": "Search Project",
        }

        if 'member_id' not in request.session:
            context["title"] = "Sign In"
            template_name = "member/sign_in.html"
        else:

            # ---------------------------------------------------------------------
            #  get default items
            # ---------------------------------------------------------------------
            # get common code
            code002 = CommonDao.select_code_list("002")
            code004 = CommonDao.select_code_list("004")

            # setting context
            context["code002"] = code002
            context["code004"] = code004

            # ---------------------------------------------------------------------
            #  get project list
            # ---------------------------------------------------------------------
            #  get parameters
            if "txtPIInit" in request.POST:
                str_pi_initial = request.POST["txtPIInit"]
                context["txtPIInit"] = str_pi_initial

            if "txtPIName" in request.POST:
                str_pi_name = request.POST["txtPIName"]
                context["txtPIName"] = str_pi_name

            if "selAnimalType" in request.POST:
                str_animal_type = request.POST["selAnimalType"]
                context["selAnimalType"] = str_animal_type

            if "selYear" in request.POST:
                str_year = request.POST["selYear"]
                context["selYear"] = str_year

            if "txtProjectAim" in request.POST:
                str_project_aim = request.POST["txtProjectAim"]
                context["txtProjectAim"] = str_project_aim

            if "txtPage" in request.POST:
                str_page = request.POST["txtPage"]
                context["txtPage"] = str_page
            else:
                str_page = 1

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
            context["resultList"] = result_list

    except Exception as e:
        r = PjoException(exception=e, user_id=request.session.get("member_id"))
        r.process()
        messages.error(request, r.message)

    return render(request, template_name, context)


'''
##########################################################################################################
#  [Raw] 
##########################################################################################################
'''


# ==============================================================================
#  Register Raw
# ==============================================================================
def raw_register(request):

    try:
        template_name = "raw/raw_list.html"
        context = {
            "title": "Raw Files",
        }

        if 'member_id' not in request.session:
            context["title"] = "Sign In"
            template_name = "member/sign_in.html"
        else:
            path_raw = Properties.path_raw()
            logger.debug("path_raw==[{}]".format(path_raw))

            member_id = request.session.get("member_id")

            # values
            dic_raw = dict()
            dic_raw["regId"] = member_id
            dic_raw["regDate"] = CommonUtil.f_get_date_time()

            # Return
            dic_result = dict()

            # Make a file list from the directory
            if not os.path.isdir(path_raw):
                raise Exception("Path does not exist. path=[" + path_raw + "]")

            list_raw = os.listdir(path_raw)
            num_insert = 0

            # ----------------------------------------------
            #  List of raw_file
            for raw_file in list_raw:
                file_nm = re.split(".zip", raw_file)
                if len(file_nm) > 1:

                    # Check DB
                    list_raw = RawDao.select_raw_list_by_name(file_nm[0])
                    len_raw = len(list_raw)
                    logger.debug("# file list ===> {}=len:[{}]".format(file_nm[0], len_raw))

                    if len_raw == 0:
                        path_study = os.path.join(path_raw, raw_file)
                        obj_study = Study(path_study, log_handler=logger)
                        obj_study.get_study_param()

                        if obj_study.subject is None:
                            continue

                        # --[DB RAW]--
                        save_time = os.path.getmtime(path_study)
                        save_time = datetime.datetime.fromtimestamp(save_time)
                        save_time = save_time.strftime("%Y%m%d")
                        dic_raw["rawFolderNm"] = file_nm[0]
                        dic_raw["rawSaveDate"] = save_time
                        dic_raw["rawSubjectId"] = obj_study.subject["SUBJECT_id"][0:20]
                        dic_raw["rawResearcher"] = obj_study.subject["SUBJECT_name_string"][0:50]
                        dic_raw["rawSpecimen"] = obj_study.subject["SUBJECT_type"][0:10]
                        dic_raw["rawGender"] = obj_study.subject["SUBJECT_sex"][0:10]
                        dic_raw["rawWeight"] = obj_study.subject["SUBJECT_weight"]
                        dic_raw["rawDeliveryDate"] = obj_study.subject["SUBJECT_dbirth"][0:12]

                        # Insert DB
                        raw_id = RawDao.insert_raw(dic_raw)
                        logger.debug("# raw_id==[{}]".format(raw_id))
                        num_insert = num_insert + 1

                        # ----------------------------------------------
                        #  List of scan
                        list_scan = obj_study.scan_list
                        for scan_no in list_scan:
                            obj_scan = obj_study.get_scan(scan_no)
                            obj_scan.get_scan_param()

                            if obj_scan.method is None:
                                continue
                            if obj_scan.acqp is None:
                                continue

                            # --[DB RAW_SCAN]--
                            dic_raw_scan = dict()
                            dic_raw_scan["regId"] = member_id
                            dic_raw_scan["regDate"] = CommonUtil.f_get_date_time()
                            dic_raw_scan["rawId"] = raw_id
                            dic_raw_scan["scan_num"] = scan_no
                            dic_raw_scan["method"] = obj_scan.method["scan_method"]
                            dic_raw_scan["tr"] = obj_scan.method["tr"]
                            dic_raw_scan["te"] = obj_scan.method["te"]
                            dic_raw_scan["band_width"] = obj_scan.method["band_width"]
                            dic_raw_scan["flip_angle"] = obj_scan.acqp["ACQ_flip_angle"]
                            dic_raw_scan["fid"] = obj_scan.fid

                            # Insert DB
                            raw_scan_id = RawDao.insert_raw_scan(dic_raw_scan)

                            if obj_scan.fid == "N":
                                continue

                            # ----------------------------------------------
                            #  List of recon
                            list_recon = obj_scan.recon_list
                            for recon_no in list_recon:
                                obj_recon = obj_scan.get_recon(recon_no)
                                obj_recon.get_param()

                                if obj_recon.visu_pars is None:
                                    continue
                                if obj_recon.reco is None:
                                    continue

                                obj_conv = obj_recon.get_conversion()

                                # resolution
                                resol = obj_conv.get_resol()
                                logger.debug("# [views.raw_register] resolution ==[{}]".format(resol))

                                # --[DB RAW_RESCAN]--
                                dic_raw_recon = dict()
                                dic_raw_recon["regId"] = member_id
                                dic_raw_recon["regDate"] = CommonUtil.f_get_date_time()
                                dic_raw_recon["rawScanId"] = raw_scan_id
                                dic_raw_recon["byteOrder"] = obj_recon.visu_pars["VisuCoreByteOrder"]
                                dic_raw_recon["wordType"] = obj_recon.visu_pars["VisuCoreWordType"]
                                dic_raw_recon["reconNum"] = recon_no
                                dic_raw_recon["resolution"] = resol
                                dic_raw_recon["matrix"] = obj_recon.visu_pars["VisuCoreSize"]
                                dic_raw_recon["fov"] = obj_recon.visu_pars["VisuCoreExtent"]
                                dic_raw_recon["thickness"] = obj_recon.recon_var["dist"]

                                # Insert DB
                                raw_recon_id = RawDao.insert_raw_recon(dic_raw_recon)

            if num_insert == 0:
                dic_result["ret_code"] = "I"
                dic_result["ret_level"] = CommonUtil.f_get_message_tag(messages.DEBUG)
                dic_result["ret_msg"] = "There is no raw folder to save."
            else:
                dic_result["ret_code"] = "I"
                dic_result["ret_level"] = CommonUtil.f_get_message_tag(messages.SUCCESS)
                dic_result["ret_msg"] = "Raw Registration success. [Success:" + str(num_insert) + "]"

    except Exception as e:
        r = PjoException(exception=e, user_id=request.session.get("member_id"))
        r.process()
        dic_result["ret_code"] = "F"
        dic_result["ret_level"] = CommonUtil.f_get_message_tag(messages.WARNING)
        dic_result["ret_msg"] = r.message

    return JsonResponse(dic_result)


# ==============================================================================
#  Raw Folder List
# ==============================================================================
def raw_search(request):

    try:
        template_name = "raw/raw_list.html"
        context = {
            "title": "Raw Files",
        }

        if 'member_id' not in request.session:
            context["title"] = "Sign In"
            template_name = "member/sign_in.html"
        else:

            # ---------------------------------------------------------------------
            #  get project list
            # ---------------------------------------------------------------------
            #  get parameters
            if "txtRawFileNm" in request.POST:
                str_raw_file = request.POST["txtRawFileNm"]
                context["txtRawFileNm"] = str_raw_file

            if "txtStartScanDate" in request.POST:
                str_start_date = request.POST["txtStartScanDate"]
                context["txtStartScanDate"] = str_start_date
                if str_start_date != "":
                    arr_start_date = str_start_date.split("/")
                    context["txtStartDate"] = arr_start_date[2] + arr_start_date[0] + arr_start_date[1]

            if "txtEndScanDate" in request.POST:
                str_end_date = request.POST["txtEndScanDate"]
                context["txtEndScanDate"] = str_end_date
                if str_end_date != "":
                    arr_end_date = str_end_date.split("/")
                    context["txtEndDate"] = arr_end_date[2] + arr_end_date[0] + arr_end_date[1]

            if "txtPage" in request.POST:
                str_page = request.POST["txtPage"]
                context["txtPage"] = str_page
            else:
                str_page = 1

            # Get Raw List
            result_list = RawDao.select_raw_list(context)

            # Paginator
            paginator = Paginator(result_list, 20)

            try:
                result_list = paginator.page(str_page)
            except PageNotAnInteger:
                result_list = paginator.page(1)
            except EmptyPage:
                result_list = paginator.page(paginator.num_pages)

            # context setting
            context["resultList"] = result_list

    except Exception as e:
        r = PjoException(exception=e, user_id=request.session.get("member_id"))
        r.process()
        messages.error(request, r.message)

    return render(request, template_name, context)


# ==============================================================================
#  Raw Study List
# ==============================================================================
def raw_study(request):

    try:

        template_name = "raw/raw_study.html"
        context = {
            "title": "Study",
        }

        if 'member_id' not in request.session:
            context["title"] = "Sign In"
            template_name = "member/sign_in.html"
        else:

            # ---------------------------------------------------------------------
            #  get project list
            # ---------------------------------------------------------------------
            #  get parameters
            if "txtRawId" in request.POST:
                str_raw_id = request.POST["txtRawId"]
                context["txtRawId"] = str_raw_id

            if "txtRawFileNm" in request.POST:
                str_raw_file = request.POST["txtRawFileNm"]
                context["txtRawFileNm"] = str_raw_file

            if "txtStartScanDate" in request.POST:
                str_start_date = request.POST["txtStartScanDate"]
                context["txtStartScanDate"] = str_start_date
                if str_start_date != "":
                    arr_start_date = str_start_date.split("/")
                    context["txtStartDate"] = arr_start_date[2] + arr_start_date[0] + arr_start_date[1]

            if "txtEndScanDate" in request.POST:
                str_end_date = request.POST["txtEndScanDate"]
                context["txtEndScanDate"] = str_end_date
                if str_end_date != "":
                    arr_end_date = str_end_date.split("/")
                    context["txtEndDate"] = arr_end_date[2] + arr_end_date[0] + arr_end_date[1]

            if "txtPage" in request.POST:
                str_page = request.POST["txtPage"]
                context["txtPage"] = str_page
            else:
                str_page = 1

            # values
            logger.debug("raw_id [" + str_raw_id + "]")
            logger.debug("txtRawFileNm [" + str_raw_file + "]")

            # Raw (Subject Info)
            obj_raw = RawDao.select_raw_object(str_raw_id)

            # setting context
            context["raw_id"] = str_raw_id
            context["raw_folder_nm"] = obj_raw.raw_folder_nm
            context["raw_save_date"] = obj_raw.raw_save_date
            context["raw_subject_id"] = obj_raw.raw_subject_id
            context["raw_researcher"] = obj_raw.raw_researcher
            context["raw_specimen"] = obj_raw.raw_specimen
            context["raw_gender"] = obj_raw.raw_gender
            context["raw_age"] = obj_raw.raw_age
            context["raw_weight"] = obj_raw.raw_weight
            context["raw_delivery_date"] = obj_raw.raw_delivery_date

            # Scan List
            scan_list = RawDao.select_raw_scan_list(str_raw_id, "", "")
            context["scan_list"] = scan_list

    except Exception as e:
        r = PjoException(exception=e, user_msg="[raw_study] Error occurred.",
                         user_id=request.session.get("member_id"))
        r.process()
        messages.error(request, r.message)

    return render(request, template_name, context)


'''
##########################################################################################################
#  [Project-Raw Mapping] 
##########################################################################################################
'''


# ==============================================================================
#  set Navigation
# ==============================================================================
def navigation(context):

    project_id = context["navProjectId"]

    # ---------------------------------------------------------------------
    # Select Project
    # ---------------------------------------------------------------------
    dic_project = ProjectDao.select_project_info(project_id)
    context["piInitial"] = dic_project["INITIAL_NM"]
    context["researcher"] = dic_project["RESEARCHER"]
    context["animalType"] = dic_project["ANIMAL_TYPE"]
    context["animalTypeNm"] = dic_project["ANIMAL"]
    context["strainType"] = dic_project["STRAIN_TYPE"]
    context["strainTypeNm"] = dic_project["STRAIN"]
    context["classification"] = dic_project["CLASSIFICATION"]
    context["year"] = dic_project["YEAR"]
    context["projectAim"] = dic_project["PROJECT_AIM"]
    context["stepCode"] = dic_project["STEP_CODE"]

    # ---------------------------------------------------------------------
    #  navigation active or deactive
    # ---------------------------------------------------------------------
    nav_stage = int(context["navStage"])
    step_code = int(context["stepCode"])+1

    len_nav = 4
    arr_nav = [0 for i in range(len_nav)]
    arr_nav[:step_code] = [1 for i in range(step_code)]
    arr_nav[nav_stage] = 2
    logger.debug("arrNav1=[{}]".format(arr_nav))
    context["arrNav1"] = arr_nav[0]
    context["arrNav2"] = arr_nav[1]
    context["arrNav3"] = arr_nav[2]
    context["arrNav4"] = arr_nav[3]


# ==============================================================================
#  Project - Raw List
# ==============================================================================
def mapping_raw_list(request):

    try:

        template_name = "mapping/mapping.html"
        context = {
            "title": "Project",
        }

        if 'member_id' not in request.session:
            context["title"] = "Sign In"
            template_name = "member/sign_in.html"
        else:

            # Set project_id
            if "navProjectId" in request.POST:
                project_id = request.POST["navProjectId"]
                logger.debug("project_id [" + project_id + "]")
            else:
                project_id = ""
            context["navProjectId"] = project_id

            # Navigation
            context['navStage'] = 0
            navigation(context)

            # ---------------------------------------------------------------------
            #  get raw list
            # ---------------------------------------------------------------------
            #  get parameters
            if "txtRawFileNm" in request.POST:
                str_raw_file = request.POST["txtRawFileNm"]
                context["txtRawFileNm"] = str_raw_file

            if "txtStartScanDate" in request.POST:
                str_start_date = request.POST["txtStartScanDate"]
                context["txtStartScanDate"] = str_start_date
                if str_start_date != "":
                    arr_start_date = str_start_date.split("/")
                    context["txtStartDate"] = arr_start_date[2] + arr_start_date[0] + arr_start_date[1]

            if "txtEndScanDate" in request.POST:
                str_end_date = request.POST["txtEndScanDate"]
                context["txtEndScanDate"] = str_end_date
                if str_end_date != "":
                    arr_end_date = str_end_date.split("/")
                    context["txtEndDate"] = arr_end_date[2] + arr_end_date[0] + arr_end_date[1]

            # Get Raw List
            result_list = RawDao.select_raw_list(context)
            context["resultList"] = result_list

    except Exception as e:
        r = PjoException(exception=e, user_msg="[mapping_raw_list] Error occurred.",
                         user_id=request.session.get("member_id"))
        r.process()
        messages.error(request, r.message)

    return render(request, template_name, context)


# ==============================================================================
#  Mapping - Raw Register
# ==============================================================================
def mapping_raw_register(request):

    try:
        template_name = "mapping/scan_info_filling.html"
        context = {
            "title": "Project",
        }

        if 'member_id' not in request.session:
            context["title"] = "Sign In"
            template_name = "member/sign_in.html"
        else:

            # values
            project_id = request.POST["navProjectId"]
            context["navProjectId"] = project_id
            logger.debug("project_id [" + project_id + "]")

            # Project Object
            project = ProjectDao.select_project_object(project_id)

            if project.derive_yn == "Y":
                raise Exception("This project is already derived.")

            choose_raw = request.POST["hidChooseRaw"]
            arr_raw = choose_raw.split(":")

            reg_id = request.session["member_id"]
            logger.debug("reg_id [" + reg_id + "]")

            # Dao
            if project_id:

                # ---------------------------------------------------------------------
                # Insert Subject
                # ---------------------------------------------------------------------
                dic_subject = dict()
                dic_subject['regId'] = reg_id
                dic_subject['regDate'] = CommonUtil.f_get_date_time()

                for raw_id in arr_raw:
                    if raw_id != "":
                        raw_obj = RawDao.select_raw_object(raw_id)
                        dic_subject['projectId'] = project_id
                        dic_subject['rawId'] = raw_id
                        dic_subject['subjectNm'] = raw_obj.raw_subject_id

                        subject_id = ProjectDao.insert_subject(dic_subject)
                        logger.debug("[insert] subject_id=[{}]".format(subject_id))

                        ProjectDao.update_project_step(project_id, 1)

                # Set context of scan list
                get_scan_list(context)

    except Exception as e:
        r = PjoException(exception=e, user_id=request.session.get("member_id"))
        r.process()
        messages.error(request, r.message)

    return render(request, template_name, context)


# ==============================================================================
#  Set Scan List Context
# ==============================================================================
def get_scan_list(context):

    # Navigation
    context['navStage'] = 1
    navigation(context)

    project_id = context["navProjectId"]

    # Dao
    if project_id:

        # ---------------------------------------------------------------------
        # Select Subject & Raw
        # ---------------------------------------------------------------------
        list_subject = ProjectDao.select_subject_raw(project_id)
        context["subjectList"] = list_subject

        # ---------------------------------------------------------------------
        # Select Scans
        # ---------------------------------------------------------------------
        if "hidRawId" in context:
            raw_id = context["hidRawId"]
        else:
            raw_id = ""

        if raw_id == "":
            if len(list_subject) > 0:
                raw_id = list_subject[0]["ID"]
                context["hidRawId"] = raw_id
                context["hidSubjectId"] = list_subject[0]["SUBJECT_ID"]
            else:
                raise Exception("RawID does not exist.")

        list_scan = ProjectDao.select_scan_list(raw_id)
        context["scanList"] = list_scan
        context["hidRawId"] = raw_id


# ==============================================================================
#  Scan Info Filling - Scan List
# ==============================================================================
def filling_scan_list(request):

    try:

        template_name = "mapping/scan_info_filling.html"
        context = {
            "title": "Project",
        }

        if 'member_id' not in request.session:
            context["title"] = "Sign In"
            template_name = "member/sign_in.html"
        else:

            # Set project_id
            if "navProjectId" in request.POST:
                project_id = request.POST["navProjectId"]
                logger.debug("project_id [" + project_id + "]")
            else:
                project_id = ""
            context["navProjectId"] = project_id

            # Set RawId
            if "hidRawId" in request.POST:
                raw_id = request.POST["hidRawId"]
                subject_id = request.POST["hidSubjectId"]
            else:
                raw_id = ""
                subject_id = ""
            context["hidRawId"] = raw_id
            context["hidSubjectId"] = subject_id

            # Set context of scan list
            get_scan_list(context)

    except Exception as e:
        r = PjoException(exception=e, user_id=request.session.get("member_id"))
        r.process()
        messages.error(request, r.message)

    return render(request, template_name, context)


# ==============================================================================
#  Modify Subject Name
# ==============================================================================
def filling_subject_modify(request):

    try:
        template_name = "mapping/scan_info_filling.html"
        context = {
            "title": "Project",
        }

        if 'member_id' not in request.session:
            context["title"] = "Sign In"
            template_name = "member/sign_in.html"
        else:

            # values
            project_id = request.POST["txtProjectId"]
            logger.debug("project_id [" + project_id + "]")

            # Project Object
            project = ProjectDao.select_project_object(project_id)

            if project.derive_yn == "Y":
                raise Exception("This project is already derived.")

            subject_id = request.POST["txtSubjectId"]
            subject_nm = request.POST["txtSubjectNm"]
            logger.debug("## subject_id=={}-{}".format(subject_id, subject_nm))

            # Return
            dic_result = dict()

            # Set Dictionary
            dic_subject = dict()
            dic_subject["subjectId"] = subject_id
            dic_subject["subjectNm"] = subject_nm

            # Update
            ProjectDao.update_subject(dic_subject)

            dic_result["ret_code"] = "U"
            dic_result["ret_level"] = CommonUtil.f_get_message_tag(messages.SUCCESS)
            dic_result["ret_msg"] = "Subject Modification success."

    except Exception as e:
        r = PjoException(exception=e, user_msg="[filling_subject_modify] Error occurred.",
                         user_id=request.session.get("member_id"))
        r.process()
        dic_result["ret_code"] = "F"
        dic_result["ret_level"] = CommonUtil.f_get_message_tag(messages.WARNING)
        dic_result["ret_msg"] = r.message

    return JsonResponse(dic_result)


# ==============================================================================
#  Get Scan Detail
# ==============================================================================
def get_scan_detail(request):

    try:
        template_name = "mapping/scan_info_filling.html"
        context = {
            "title": "Project",
        }

        if 'member_id' not in request.session:
            context["title"] = "Sign In"
            template_name = "member/sign_in.html"
        else:

            # Values
            raw_id = request.POST["txtRawId"]
            raw_scan_id = request.POST["txtScanId"]
            raw_recon_id = request.POST["txtReconId"]
            logger.debug("## raw_id=={}, scan_id={}, recon_id={}".format(raw_id, raw_scan_id, raw_recon_id))

            # Select Scan
            scan = RawDao.select_raw_scan_list(raw_id, raw_scan_id, raw_recon_id)
            json_str = json.dumps(scan)

    except Exception as e:
        r = PjoException(exception=e, user_msg="[filling_subject_modify] Error occurred.",
                         user_id=request.session.get("member_id"))
        r.process()

    return HttpResponse(json_str, content_type="application/json")


# ==============================================================================
#  Register Raw_scan, Raw_recon
# ==============================================================================
def scan_register(request):

    try:
        template_name = "mapping/scan_info_filling.html"
        context = {
            "title": "Project",
        }

        if 'member_id' not in request.session:
            context["title"] = "Sign In"
            template_name = "member/sign_in.html"
        else:

            # values
            project_id = request.POST["txtProjectId"]
            logger.debug("project_id [" + project_id + "]")

            # Project Object
            project = ProjectDao.select_project_object(project_id)

            if project.derive_yn == "Y":
                raise Exception("This project is already derived.")

            # Return
            dic_result = dict()

            # reg_id
            reg_id = request.session["member_id"]
            logger.debug("reg_id [" + reg_id + "]")

            # Set Dictionary
            dic_scan = dict()
            dic_scan["projectId"] = project_id
            dic_scan["subjectId"] = request.POST["txtSubjectId"]
            dic_scan["rawScanId"] = request.POST["txtRawScanId"]
            dic_scan["rawReconId"] = request.POST["txtRawReconId"]
            dic_scan["sessionId"] = request.POST["txtSesId"]
            dic_scan["sessionNm"] = request.POST["txtSesNm"]
            dic_scan["scanId"] = request.POST["txtScanId"]
            dic_scan["task"] = request.POST["txtTask"]
            dic_scan["acq"] = request.POST["txtAcq"]
            dic_scan["ce"] = request.POST["txtCe"]
            dic_scan["rec"] = request.POST["txtRec"]
            dic_scan["aim"] = request.POST["txtAim"]
            dic_scan['regId'] = reg_id
            dic_scan['regDate'] = CommonUtil.f_get_date_time()
            logger.debug("## scan_id=={}, recon_id={}".format(dic_scan["rawScanId"], dic_scan["rawReconId"]))

            if dic_scan["sessionId"] == "":

                # Insert Session
                session_id = ProjectDao.insert_session(dic_scan)
                dic_scan["sessionId"] = session_id
                logger.debug("# Session Id={}".format(session_id))

                # Insert Scan
                scan_id = ProjectDao.insert_scan(dic_scan)
                logger.debug("# Scan Id={}".format(scan_id))

                # Update Project
                ProjectDao.update_project_step(dic_scan["projectId"], 2)

            else:
                # Update Session
                ProjectDao.update_session(dic_scan)

                # Update Scan
                ProjectDao.update_scan(dic_scan)

                session_id = dic_scan["sessionId"]
                scan_id = dic_scan["scanId"]

            # Result
            dic_result["session_id"] = session_id
            dic_result["scan_id"] = scan_id
            dic_result["ret_code"] = "U"
            dic_result["ret_level"] = CommonUtil.f_get_message_tag(messages.SUCCESS)
            dic_result["ret_msg"] = "Scan Info registration success."

    except Exception as e:
        r = PjoException(exception=e, user_id=request.session.get("member_id"))
        r.process()
        dic_result["ret_code"] = "F"
        dic_result["ret_level"] = CommonUtil.f_get_message_tag(messages.WARNING)
        dic_result["ret_msg"] = r.message

    return JsonResponse(dic_result)


# ==============================================================================
#  Delete Raw_scan, Raw_recon
# ==============================================================================
def scan_delete(request):

    try:
        template_name = "mapping/scan_info_filling.html"
        context = {
            "title": "Project",
        }

        if 'member_id' not in request.session:
            context["title"] = "Sign In"
            template_name = "member/sign_in.html"
        else:

            # values
            project_id = request.POST["txtProjectId"]
            logger.debug("project_id [" + project_id + "]")

            # Project Object
            project = ProjectDao.select_project_object(project_id)

            if project.derive_yn == "Y":
                raise Exception("This project is already derived.")

            # Return
            dic_result = dict()

            # reg_id
            reg_id = request.session["member_id"]
            logger.debug("reg_id [" + reg_id + "]")

            # Set Dictionary
            session_id = request.POST["txtSesId"]
            scan_id = request.POST["txtScanId"]
            logger.debug("## sessionId=={}, scanId={}".format(session_id, scan_id))

            if session_id == "":
                raise Exception("Session Id does not exist. ")
            if scan_id == "":
                raise Exception("Scan Id does not exist. ")

            # Delete Scan
            ProjectDao.delete_scan(scan_id)

            # Delete Session
            ProjectDao.delete_session(session_id)

            # Result
            dic_result["ret_code"] = "U"
            dic_result["ret_level"] = CommonUtil.f_get_message_tag(messages.SUCCESS)
            dic_result["ret_msg"] = "Scan Info registration success."

    except Exception as e:
        r = PjoException(exception=e, user_id=request.session.get("member_id"))
        r.process()
        dic_result["ret_code"] = "F"
        dic_result["ret_level"] = CommonUtil.f_get_message_tag(messages.WARNING)
        dic_result["ret_msg"] = r.message

    return JsonResponse(dic_result)




