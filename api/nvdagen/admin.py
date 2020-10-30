from django.contrib import admin
from .models import Listing, Business, Sponsor, TeamMember, Form

# Register your models here.
admin.site.register(Listing)
admin.site.register(TeamMember)
admin.site.register(Business)
admin.site.register(Sponsor)
admin.site.register(Form)
