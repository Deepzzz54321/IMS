from django.db import models

# Create your models here.
class Rooms(models.Model):
    room_id = models.CharField(primary_key=True, max_length=15, null=False)
    name = models.CharField(max_length=50, null=False),
    requirements = models.TextField(null=True, blank=True)

class Employees(models.Model):
    BRANCH = (
        ('CSE','CSE'),
        ('ECE','ECE'),
        ('EEE','EEE'),
        ('BIOTECH','BIOTECH'),
        ('MECH','MECH'),
        ('CIVIL','CIVIL'),
        ('MME','MME'),
        ('CHEM','CHEM'),
        ('SHM', 'SHM'),
        ('SOS','SOS'),
        ('Administration Section', 'Administration Section'),
        ('Admissions Section', 'Admissions Section'),
        ('Exam Section', 'Exam Section'),
        ('T&P Cell', 'T&P Cell'),
        ('Research Cell', 'Research Cell'),
        ('Planning & Development Section', 'Planning & Development Section'),
        ('Student Affairs Section', 'Student Affairs Section'),
        ('Financial Section', 'Financial Section'),
        ('Inventory Section', 'Inventory Section'),
        ('Sales & Purchases Section', 'Sales & Purchases Section'),
        ('Medical Section', 'Medical Section'),
        ('Boys Hostels','Boys Hostels'),
        ('Girls Hostels', 'Girls Hostels'),

    )

    emp_id = models.IntegerField(primary_key=True, null=False)
    name = models.CharField(max_length=100, null=False)
    branch = models.CharField(max_length=100,choices=BRANCH, null=False)
    designation = models.CharField(max_length=100, null=False)
    room_id = models.ForeignKey(Rooms,on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(max_length=10,null=False)
    email_id = models.CharField(max_length=50, null=False)

    def __str__(self):
        return str(self.emp_id)

class Products(models.Model):
    STATUS = (
        ('Usable','Usable'),
        ('Maintenance','Maintenance'),
        ('Unusable','Unusable'),
    )

    BRANCH = (
        ('CSE','CSE'),
        ('ECE','ECE'),
        ('EEE','EEE'),
        ('BIOTECH','BIOTECH'),
        ('MECH','MECH'),
        ('CIVIL','CIVIL'),
        ('MME','MME'),
        ('CHEM','CHEM'),
        ('SHM', 'SHM'),
        ('SOS','SOS'),
        ('Administration Section', 'Administration Section'),
        ('Admissions Section', 'Admissions Section'),
        ('Exam Section', 'Exam Section'),
        ('T&P Cell', 'T&P Cell'),
        ('Research Cell', 'Research Cell'),
        ('Planning & Development Section', 'Planning & Development Section'),
        ('Student Affairs Section', 'Student Affairs Section'),
        ('Financial Section', 'Financial Section'),
        ('Inventory Section', 'Inventory Section'),
        ('Sales & Purchases Section', 'Sales & Purchases Section'),
        ('Medical Section', 'Medical Section'),
        ('Boys Hostels','Boys Hostels'),
        ('Girls Hostels', 'Girls Hostels'),

    )

    prod_id = models.CharField(primary_key=True, max_length=15, null=False)
    name = models.CharField(max_length=30, null=False)
    type = models.CharField(max_length=20, null=False)
    status = models.CharField(max_length=15,null=False, choices=STATUS, default='Usable')
    branch = models.CharField(max_length=100,choices=BRANCH, null=True,blank=True)
    room_id = models.ForeignKey(Rooms,on_delete=models.CASCADE, null=True, blank=True)
    specs = models.TextField(null=True, blank=True)
    update = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.prod_id)


class Requests(models.Model):

    BRANCH = (
        ('CSE','CSE'),
        ('ECE','ECE'),
        ('EEE','EEE'),
        ('BIOTECH','BIOTECH'),
        ('MECH','MECH'),
        ('CIVIL','CIVIL'),
        ('MME','MME'),
        ('CHEM','CHEM'),
        ('SHM', 'SHM'),
        ('SOS','SOS'),
        ('Administration Section', 'Administration Section'),
        ('Admissions Section', 'Admissions Section'),
        ('Exam Section', 'Exam Section'),
        ('T&P Cell', 'T&P Cell'),
        ('Research Cell', 'Research Cell'),
        ('Planning & Development Section', 'Planning & Development Section'),
        ('Student Affairs Section', 'Student Affairs Section'),
        ('Financial Section', 'Financial Section'),
        ('Inventory Section', 'Inventory Section'),
        ('Sales & Purchases Section', 'Sales & Purchases Section'),
        ('Medical Section', 'Medical Section'),
        ('Boys Hostels','Boys Hostels'),
        ('Girls Hostels', 'Girls Hostels'),

    )

    STATUS=(
        ('Pending','Pending'),
        ('Resolved','Resolved'),
    )

    branch = models.CharField(max_length=100,choices=BRANCH, null=False)
    type = type = models.CharField(max_length=20, null=False)
    specs = models.TextField(null=True, blank=True)
    count = models.IntegerField(null=False)
    status = models.CharField(max_length=20,choices=STATUS,null=False,default='Pending')

