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

    # about Project
    path('prj_frm', views.project_form, name='prj_frm'),
    path('prj_mod/<project_id>', views.project_modify, name='prj_mod'),
    path('prj_reg', views.project_register, name='prj_reg'),

    path('prj_sch', views.project_search, name='prj_sch'),

    # about Raw
    path('raw_frm', views.raw_register, name='raw_frm'),
    path('raw_reg', views.raw_register, name='raw_reg'),

]
