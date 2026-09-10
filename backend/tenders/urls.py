from rest_framework.routers import DefaultRouter
from .views import TenderViewSet,TenderDocumentViewSet,TenderItemViewSet
router=DefaultRouter()
router.register("items",TenderItemViewSet,basename="tender-item")
router.register("documents",TenderDocumentViewSet,basename="document")
router.register("",TenderViewSet,basename="tender")
urlpatterns=router.urls
