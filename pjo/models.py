from django.db import models
from django.utils import timezone
from django import forms



YN_TYPE = (
     ('Y', 'YES')
     , ('N', 'NO')
)

USE_TYPE = (
     ('Y', 'USE')
     , ('N', 'NOT USE')
)

AUTH_TYPE = (
     ('10', 'Common User')
     , ('99', 'Administrator')
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
    group_id = models.ForeignKey(CodeGroup, on_delete=models.CASCADE)
    code_id = models.CharField(max_length=2)
    code_nm = models.CharField(max_length=30)
    upper_id = models.CharField(max_length=3)
    order_no = models.CharField(max_length=2)


"""
==============================================
2. Managing of Members
==============================================
"""


class Researcher(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    first_nm = models.CharField(max_length=50)
    last_nm = models.CharField(max_length=50)
    initial_nm = models.CharField(max_length=2)
    password = models.CharField(max_length=20)
    authority = models.CharField(max_length=2, default='10', choices=AUTH_TYPE)
    reg_date = models.DateTimeField()


"""
==============================================
3. Managing of Projects
==============================================
"""


class Project(models.Model):
    project_id = models.CharField(max_length=4, primary_key=True)
    initial_nm = models.CharField(max_length=2)
    animal_type = models.CharField(max_length=1)
    strain_type = models.CharField(max_length=1)
    classification = models.CharField(max_length=5)
    year = models.CharField(max_length=4)
    researcher_nm = models.CharField(max_length=50)
    project_aim = models.CharField(max_length=50)
    status_code = models.CharField(max_length=1)
    reg_id = models.CharField(max_length=20, default='admin')
    reg_date = models.DateTimeField(default=timezone.now)


class Subject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    subject_nm = models.CharField(max_length=20)
    single_ses_yn = models.CharField(max_length=1, default='Y', choices=USE_TYPE)
    reg_id = models.CharField(max_length=20, default='admin')
    reg_date = models.DateTimeField(default=timezone.now)


class Session(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    session_nm = models.CharField(max_length=20, default='normal')
    reg_id = models.CharField(max_length=20, default='admin')
    reg_date = models.DateTimeField(default=timezone.now)


class Scan(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    scan_num = models.CharField(max_length=2)
    data_type = models.CharField(max_length=1)
    reg_id = models.CharField(max_length=20, default='admin')
    reg_date = models.DateTimeField(default=timezone.now)







