from django.db import models
from institute.models import Employees


# Create your models here.
class credentials(models.Model):
    emp_id = models.ForeignKey(Employees,on_delete=models.CASCADE, null=False)
    password = models.CharField(max_length=25,null=False)

    def __str__(self):
            return str(self.emp_id)

