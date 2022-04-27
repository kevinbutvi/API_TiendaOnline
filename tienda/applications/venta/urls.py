from django.urls import path
from . import views


app_name = "venta_app"

urlpatterns = [
    path(
        'api/venta/reporte/',
        views.ReporteVentasList.as_view(),
        name="venta_reporte"
        ),
    path(
        'api/venta/add/',
        views.RegistrarVenta.as_view(),
        name="venta_creacion"
        ),
]