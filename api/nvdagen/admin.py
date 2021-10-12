from django.contrib import admin
from .models import Listing, Business, Sponsor, TeamMember, Form, Program, Participant


# Register your models here.
admin.site.register(Listing)
admin.site.register(TeamMember)
admin.site.register(Business)
admin.site.register(Sponsor)
admin.site.register(Form)
admin.site.register(Program)
admin.site.register(Participant)
