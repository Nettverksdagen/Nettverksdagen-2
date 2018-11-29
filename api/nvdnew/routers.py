from rest_framework import routers
from nvdagen.viewsets import ListingViewSet, BusinessViewSet

router = routers.DefaultRouter()

router.register(r'listing', ListingViewSet)
router.register(r'business', BusinessViewSet)
