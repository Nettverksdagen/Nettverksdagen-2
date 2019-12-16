from rest_framework import routers
from nvdagen.viewsets import ListingViewSet, BusinessViewSet, SponsorViewSet, TeamMemberViewSet, FormViewSet

router = routers.DefaultRouter()

router.register(r'listing', ListingViewSet)
router.register(r'teammember', TeamMemberViewSet)
router.register(r'business', BusinessViewSet)
router.register(r'sponsor', SponsorViewSet)
router.register(r'form', FormViewSet)
