from rest_framework.routers import DefaultRouter

from . import viewsets


# Se instancia del enrutador
router = DefaultRouter()

# Registro de rutas
router.register(r'ventas', viewsets.VentasViewSet, basename="ventas") 

urlpatterns = router.urls