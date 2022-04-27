from django.urls import path
from . import views


app_name = "producto_app"

urlpatterns = [
    path(
        'api/product/por-usuario/',
        views.ListProductUser.as_view(),
        name="producto-by-user"
        ),
    path(
        'api/product/en-stock/',
        views.ListProductStock.as_view(),
        name="producto-en-stock"
        ),
    path(
        'api/product/por-genero/<gender>/',
        views.ListProducGenero.as_view(),
        name="producto-by-genero"
        ),
    path(
        'api/product/filtrar/',
        views.FiltrarProductos.as_view(),
        name="producto-filtrar"
        ),
]