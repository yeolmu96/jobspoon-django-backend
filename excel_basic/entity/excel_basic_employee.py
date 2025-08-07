from django.db import models

# Create your models here.
class ExcelBasicEmployee(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField()
    city = models.CharField(max_length=64)
    score = models.IntegerField()
    department = models.CharField(max_length=32)

    class Meta:
        db_table = "excel_basic_employee"