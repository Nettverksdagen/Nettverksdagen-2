from django.db import models


class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    company_name = models.CharField(max_length=250)
    deadline = models.DateField(default="1970-01-01")
    logo_uri = models.CharField(max_length=250)
