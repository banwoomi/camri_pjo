from django.db import models
from django.utils import timezone
from django import forms


USE_TYPE = (
     ('Y', 'USE')
     , ('N', 'NOT USE')
)

AUTH_TYPE = (
     ('10', 'Common User')
     , ('99', 'Administrator')
)

STEP_TYPE = (
    ('0', 'Register')
    , ('1', 'Study Mapping')
    , ('2', 'Scan Info Filling')
    , ('3', 'Derivation')
    , ('4', 'Preprocess-start')
    , ('5', 'Preprocess-end')
)

"""
==============================================
1. Common Table
==============================================
"""


class CodeGroup(models.Model):
    group_id = models.CharField(max_length=3, primary_key=True)
    group_nm = models.CharField(max_length=30)


class Code(models.Model):
    group = models.ForeignKey(CodeGroup, on_delete=models.CASCADE)
    code_id = models.CharField(max_length=2)
    code_nm = models.CharField(max_length=30)
    upper_id = models.CharField(max_length=3, blank=True, null=True)
    order_no = models.CharField(max_length=2)


class ExceptionLog(models.Model):
    exc_name = models.CharField(max_length=40)
    exc_msg = models.CharField(max_length=100)
    filename = models.CharField(max_length=100)
    line_no = models.IntegerField(default=0)
    line_string = models.CharField(max_length=100)
    reg_id = models.CharField(max_length=20, default='anonymous')
    reg_date = models.DateTimeField(default=timezone.now)


"""
==============================================
2. Managing of Members
==============================================
"""


class Researcher(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    first_nm = models.CharField(max_length=50)
    last_nm = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    authority = models.CharField(max_length=2, default='10', choices=AUTH_TYPE)
    reg_date = models.DateTimeField()


"""
==============================================
3. Managing of Raws
==============================================
"""


class Raw(models.Model):
    raw_folder_nm = models.CharField(max_length=50)
    raw_save_date = models.CharField(max_length=8)
    raw_subject_id = models.CharField(max_length=20, blank=True, null=True)
    raw_researcher = models.CharField(max_length=50, blank=True, null=True)
    raw_specimen = models.CharField(max_length=10, blank=True, null=True)
    raw_gender = models.CharField(max_length=10, blank=True, null=True)
    raw_age = models.CharField(max_length=10, blank=True, null=True)
    raw_weight = models.CharField(max_length=10, blank=True, null=True)
    raw_delivery_date = models.CharField(max_length=12, blank=True, null=True)
    reg_id = models.CharField(max_length=20, default='anonymous')
    reg_date = models.DateTimeField(default=timezone.now)


class RawScan(models.Model):
    raw = models.ForeignKey(Raw, on_delete=models.CASCADE)
    scan_num = models.CharField(max_length=2)
    method = models.CharField(max_length=10)
    tr = models.CharField(max_length=5)
    te = models.CharField(max_length=20)
    band_width = models.CharField(max_length=20)
    flip_angle = models.CharField(max_length=5)
    fid = models.CharField(max_length=1, default='N', choices=USE_TYPE)
    reg_id = models.CharField(max_length=20, default='anonymous')
    reg_date = models.DateTimeField(default=timezone.now)


class RawRecon(models.Model):
    raw_scan = models.ForeignKey(RawScan, on_delete=models.CASCADE)
    recon_num = models.CharField(max_length=2)
    byte_order = models.CharField(max_length=20)
    word_type = models.CharField(max_length=20)
    resolution = models.CharField(max_length=100)
    matrix = models.CharField(max_length=15)
    fov = models.CharField(max_length=20)
    thickness = models.CharField(max_length=5)
    reg_id = models.CharField(max_length=20, default='anonymous')
    reg_date = models.DateTimeField(default=timezone.now)


"""
==============================================
4. Managing of Projects
==============================================
"""


class Project(models.Model):
    project_id = models.CharField(max_length=4, primary_key=True)
    initial_nm = models.CharField(max_length=2)
    animal_type = models.CharField(max_length=1)
    strain_type = models.CharField(max_length=1)
    classification = models.CharField(max_length=5)
    year = models.CharField(max_length=4)
    pi_first_nm = models.CharField(max_length=30)
    pi_last_nm = models.CharField(max_length=30)
    project_aim = models.CharField(max_length=50)
    step_code = models.CharField(max_length=1, default='0', choices=STEP_TYPE)
    derive_yn = models.CharField(max_length=1, default='N', choices=USE_TYPE)
    reg_id = models.CharField(max_length=20, default='anonymous')
    reg_date = models.DateTimeField(default=timezone.now)


class Subject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    raw = models.ForeignKey(Raw, on_delete=models.CASCADE)
    subject_nm = models.CharField(max_length=20)
    reg_id = models.CharField(max_length=20, default='anonymous')
    reg_date = models.DateTimeField(default=timezone.now)


class Session(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    raw_scan = models.ForeignKey(RawScan, on_delete=models.CASCADE)
    session_nm = models.CharField(max_length=20, default='single')
    reg_id = models.CharField(max_length=20, default='anonymous')
    reg_date = models.DateTimeField(default=timezone.now)


class Scan(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    raw_recon = models.ForeignKey(RawRecon, on_delete=models.CASCADE)
    task = models.CharField(max_length=20, blank=True, null=True)
    acq = models.CharField(max_length=20, blank=True, null=True)
    ce = models.CharField(max_length=20, blank=True, null=True)
    rec = models.CharField(max_length=2, blank=True, null=True)
    run = models.CharField(max_length=2, blank=True, null=True)
    mode = models.CharField(max_length=1, blank=True, null=True)
    aim = models.CharField(max_length=50, blank=True, null=True)
    reg_id = models.CharField(max_length=20, default='anonymous')
    reg_date = models.DateTimeField(default=timezone.now)



