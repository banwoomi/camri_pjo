from django.urls import path
from . import views

app_name = "pjo"

urlpatterns = [
    # path('admin/', admin.site.urls),

    # main
    path('', views.cam_main, name='index'),

    # about JOIN
    path('signup_frm', views.sign_up_form, name='signup_frm'),
    path('chk_id', views.check_id, name='chk_id'),
    path('sign_up', views.sign_up_form, name='sign_up'),

    # about SIGN IN
    path('sign_frm', views.sign_up_form, name='sign_frm'),
    path('sign_in', views.sign_up_form, name='sign_in'),
    path('sign_out', views.sign_up_form, name='sign_out'),

    # about Profile
    path('prf_frm', views.sign_up_form, name='prf_frm'),
    path('prf_mod', views.sign_up_form, name='prf_mod'),

]
