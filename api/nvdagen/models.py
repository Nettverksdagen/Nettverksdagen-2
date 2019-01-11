from django.db import models

SUMMER_INTERNSHIP = 'Sommerjobb'
FULL_TIME_POSITION = 'Fast stilling'
PART_TIME_POSITION = 'Deltidsstilling'
INTERNSHIP = 'Internship'
TRAINEE_POSITION = 'Trainee'
OTHER_POSITION = 'Annet'

LISTINGTYPECHOICE = (
    (SUMMER_INTERNSHIP, SUMMER_INTERNSHIP),
    (FULL_TIME_POSITION, FULL_TIME_POSITION),
    (PART_TIME_POSITION, PART_TIME_POSITION),
    (INTERNSHIP, INTERNSHIP),
    (TRAINEE_POSITION, TRAINEE_POSITION),
    (OTHER_POSITION, OTHER_POSITION)
)


class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    company_name = models.CharField(max_length=250)
    deadline = models.DateField(default="1970-01-01")
    logo_uri = models.CharField(max_length=250)
    type = models.CharField(max_length=250, choices=LISTINGTYPECHOICE, default=OTHER_POSITION)
    listing_url = models.CharField(max_length=250)
    city = models.CharField(max_length=250)


class BusinessWithLogo(models.Model):
    name = models.CharField(max_length=250)
    logo_uri = models.CharField(max_length=250)
    website_url = models.CharField(max_length=250)

    class Meta:
        abstract = True


class Business(BusinessWithLogo):
    id = models.AutoField(primary_key=True)


class Sponsor(BusinessWithLogo):
    id = models.AutoField(primary_key=True)
