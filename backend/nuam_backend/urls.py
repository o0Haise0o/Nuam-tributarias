from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from taxgrades.views import (
    TaxGradeViewSet, 
    CalificacionViewSet, 
    OrigenInformacionViewSet, 
    AuditLogViewSet
)
from django.views.generic import RedirectView


router = DefaultRouter()
router.register(r"tax-grades", TaxGradeViewSet, basename="taxgrade")
router.register(r"calificaciones", CalificacionViewSet, basename="calificacion")
router.register(r"origenes", OrigenInformacionViewSet, basename="origen")
router.register(r"audit", AuditLogViewSet, basename="audit")


urlpatterns = [
    path("", RedirectView.as_view(url="/api/", permanent=False)),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]