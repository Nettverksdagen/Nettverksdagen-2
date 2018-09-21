from django.db import models


class Listing(models.Model):
    listing_id = models.AutoField(primary_key=True)
    listing_name = models.CharField(max_length=250)
    listing_company_name = models.CharField(max_length=250)
