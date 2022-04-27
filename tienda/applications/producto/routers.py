from rest_framework.routers import DefaultRouter

from . import viewsets

# Se instancia del objeto enrutador
router = DefaultRouter()

# Registro de rutas
router.register(r'colours', viewsets.ColourViewSet, basename="colours")
router.register(r'productos', viewsets.ProductViewSet, basename="productos") 

urlpatterns = router.urls
