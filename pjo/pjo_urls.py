from django.urls import path
from . import views

app_name = "pjo"

urlpatterns = [
    # path('admin/', admin.site.urls),

    # main
    path('', views.cam_main, name='index'),

    # Common
    path('inq_cd', views.common_code_inq, name='inq_cd'),

    # about JOIN
    path('signup_frm', views.sign_up_form, name='signup_frm'),
    path('chk_id', views.check_id, name='chk_id'),
    path('sign_up', views.sign_up, name='sign_up'),

    # about SIGN IN
    path('sign_frm', views.sign_form, name='sign_frm'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('sign_out', views.sign_out, name='sign_out'),

    # about Profile
    path('prf_frm', views.profile_form, name='prf_frm'),
    path('prf_mod', views.profile_modify, name='prf_mod'),

    # about Raw
    path('raw_reg', views.raw_register, name='raw_reg'),
    path('raw_sch', views.raw_search, name='raw_sch'),
    path('raw_std', views.raw_study, name='raw_std'),

    # about Project
    path('prj_frm', views.project_form, name='prj_frm'),
    path('prj_mod/<project_id>', views.project_modify_frm, name='prj_mod'),
    path('prj_reg', views.project_register, name='prj_reg'),
    path('prj_sch', views.project_search, name='prj_sch'),

    # Mapping - Raw List
    path('map_raw', views.mapping_raw_list, name='map_raw'),
    path('map_reg', views.mapping_raw_register, name='map_reg'),

    # Filling scan info
    path('sub_lst', views.filling_scan_list, name='scan_lst'),
    path('sub_mod', views.filling_subject_modify, name='sub_mod'),
    path('scan_dtl', views.get_scan_detail, name='scan_dtl'),
    path('scan_reg', views.scan_register, name='scan_reg'),
    path('scan_del', views.scan_delete, name='scan_del'),

]
