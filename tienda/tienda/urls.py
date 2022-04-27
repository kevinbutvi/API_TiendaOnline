from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("applications.users.urls")),
    path('', include("applications.producto.urls")),
    path('', include("applications.venta.urls")),
    # Routers
    path('', include("applications.producto.routers")),
    path('', include("applications.venta.routers")),

]
