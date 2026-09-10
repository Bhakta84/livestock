from rest_framework.routers import DefaultRouter
from .views import BidViewSet,BidDocumentViewSet
router=DefaultRouter()
router.register("documents",BidDocumentViewSet,basename="bid-document")
router.register("",BidViewSet,basename="bid")
urlpatterns=router.urls
