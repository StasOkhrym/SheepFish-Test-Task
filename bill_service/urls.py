from django.urls import path, include
from .views import PointViewSet, PrinterViewSet, CheckViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("points", PointViewSet)
router.register("printers", PrinterViewSet)
router.register("checks", CheckViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "bill_service"
