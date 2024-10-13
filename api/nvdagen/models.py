from django.db import models
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status

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

MAIN_PARTNER = 'Hovedsamarbeidspartner'
PARTNER = 'Samarbeidspartner'
GOLD = 'Gull'
SILVER = 'Sølv'
BRONZE = 'Bronse'

LEVELTYPECHOICE = (
    (MAIN_PARTNER, MAIN_PARTNER),
    (PARTNER, PARTNER),
    (GOLD, GOLD),
    (SILVER, SILVER),
    (BRONZE, BRONZE)
)

DAYS_NONE = 'Ingen dager'
DAY1 = 'Dag 1'
DAY2 = 'Dag 2'
DAYS_BOTH = 'Begge dager'

DAYSCHOICE = (
    (DAYS_NONE, DAYS_NONE),
    (DAY1, DAY1),
    (DAY2, DAY2),
    (DAYS_BOTH, DAYS_BOTH)
)


class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    company_name = models.CharField(max_length=250)
    deadline = models.DateField(default=None, blank=True, null=True)
    logo_uri = models.CharField(max_length=250)
    type = models.CharField(max_length=250, choices=LISTINGTYPECHOICE, default=OTHER_POSITION)
    listing_url = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    internal_url = models.CharField(max_length=250, blank=True, null=True)
    content = models.TextField(blank=True, null=True, default='')


class TeamMember(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    photo_uri = models.CharField(max_length=250, blank=True, null=True, default='')
    team = models.CharField(max_length=250)
    position = models.CharField(max_length=250)


class BusinessWithLogo(models.Model):
    name = models.CharField(max_length=250)
    logo_uri = models.CharField(max_length=250)
    website_url = models.CharField(max_length=250)

    class Meta:
        abstract = True


class Business(BusinessWithLogo):
    id = models.AutoField(primary_key=True)
    level = models.CharField(max_length=250, choices=LEVELTYPECHOICE, default=GOLD)
    text = models.TextField()
    days = models.CharField(max_length=250, choices=DAYSCHOICE, default=DAYS_NONE)
    standnumber = models.IntegerField(default=10)


class Sponsor(BusinessWithLogo):
    id = models.AutoField(primary_key=True)

class Form(models.Model):
    id = models.AutoField(primary_key=True)
    external_url = models.CharField(max_length=250)
    internal_url = models.CharField(max_length=250)
    iframe_height = models.CharField(max_length=250)


class Program(models.Model):
    id = models.AutoField(primary_key=True)
    header = models.CharField(max_length=250)
    place = models.CharField(max_length=250)
    timeStart = models.IntegerField()
    timeEnd= models.IntegerField()
    paragraph = models.CharField(max_length=10000,blank=True, null=True)
    registration = models.BooleanField(default=False)
    maxRegistered = models.IntegerField( blank=True, null=True)
    cancelEmail = models.CharField(max_length=250, blank=True, null=True)
    registrationStart = models.IntegerField(blank=True, null=True)
    registrationEnd = models.IntegerField(blank=True, null=True)


class Participant(models.Model):
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Program, on_delete=models.CASCADE)
    email = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    year = models.CharField(max_length=250)
    study = models.CharField(max_length=250)
    code = models.CharField(max_length=250)

class SpinTheWheel(models.Model):
    id = models.AutoField(primary_key=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
