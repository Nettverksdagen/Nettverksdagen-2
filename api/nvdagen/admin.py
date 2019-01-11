from django.contrib import admin
from .models import Listing, Business, Sponsor, TeamMember

# Register your models here.
admin.site.register(Listing)
admin.site.register(TeamMember)
admin.site.register(Business)
admin.site.register(Sponsor)
