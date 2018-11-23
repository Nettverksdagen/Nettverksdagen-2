from rest_framework import routers
from nvdagen.viewsets import ListingViewSet

router = routers.DefaultRouter()

router.register(r'listing', ListingViewSet)
