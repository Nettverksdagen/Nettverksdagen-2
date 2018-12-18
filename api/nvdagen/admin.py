from django.contrib import admin
from .models import Listing, Business, Sponsor

# Register your models here.
admin.site.register(Listing)
admin.site.register(Business)
admin.site.register(Sponsor)
