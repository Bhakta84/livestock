from rest_framework.routers import DefaultRouter
from .views import BidViewSet,BidDocumentViewSet
router=DefaultRouter()
router.register("",BidViewSet,basename="bid")
router.register("documents",BidDocumentViewSet,basename="bid-document")
urlpatterns=router.urls
