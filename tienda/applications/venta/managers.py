import imp
from django.db import models


class SaleDetailManager(models.Manager):
    """ Managers para el modelo SaleDetail"""

    def Detalle_producto_ventas(self, venta_id):
        """ Detalle Por Venta """
        
        detalle = self.filter(
            sale__id = venta_id
        ).order_by('count', 'product__name')
        
        return (detalle)