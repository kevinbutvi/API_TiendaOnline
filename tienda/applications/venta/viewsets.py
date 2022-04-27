from applications.producto.models import Product
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .models import Sale, SaleDetail
from .serializers import ProcesoVentaSerializer2, VentaReporteSerializer


class VentasViewSet(viewsets.ViewSet):
    """ Viewset para Ventas y Detalles de Ventas. """

    authentication_classes = [TokenAuthentication] # Tipo de Autenticacion
    
    queryset = Sale.objects.all()
    
    def get_permissions(self):
        """ Permisos personalizados para distintas ACTIONS """

        if (self.action == 'list' or self.action == 'retrieve'):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
    
        return([permission() for permission in permission_classes]) # Retorna lista con los Permisos
    
    
    def list(self, request, *args, **kwargs):
        """ Sobreescritura LIST para mostrar lista personalizada """
        
        queryset = Sale.objects.all()
        
        serializer = VentaReporteSerializer(queryset, many=True)
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):
        """ Sobreescritura CREATE para hacer almacenamiento en DB """

        serializador = ProcesoVentaSerializer2(data=request.data) # DESERIALIZA los datos recibidos
        serializador.is_valid(raise_exception = True)
        
        # Datos ya validados
        tipo_recibo = serializador.validated_data["type_invoce"] 
        tipo_pago = serializador.validated_data["type_payment"]
        direcccion = serializador.validated_data["address_send"]
        
        # Recupero los productos de la venta
        productos = Product.objects.filter(
            id__in = serializador.validated_data["productos"]
        )
        cantidades = serializador.validated_data["cantidades"]
        
        usuario = self.request.user
        fecha = timezone.now()
        
        venta = Sale.objects.create(
            date_sale = fecha,
            amount = 0,
            count = 0,
            type_invoce = tipo_recibo,
            type_payment = tipo_pago,
            address_send = direcccion,
            user = usuario,
        )
        
        # Variables para calculos de venta
        monto = 0
        cant = 0
        
        ventas_detalle = [] # Variable que se utilizara para almacenar todos los detalles de ventas y hacer BULK_CREATE
        

        for producto, cantidad in zip(productos, cantidades):
            
            monto = (monto + producto.price_sale * cantidad)
            cant = (cant + cantidad)
            venta.amount = monto
            venta.count = cantidad
            venta.save()
            
            venta_detalle = SaleDetail(
                sale = venta,
                product = producto,
                count = cantidad,
                price_purchase = producto.price_purchase,
                price_sale = producto.price_sale,
            )
            
            # Acumulo en el array todos los detalles de ventas
            ventas_detalle.append(venta_detalle)
            
        # Se Crea el detalle de venta
        SaleDetail.objects.bulk_create(ventas_detalle)
        
        return (Response({"msj": "VENTA EXITOSA"}))


    def retrieve(self, request, pk=None):
        """ Recupera un objeto en particular segun ID """
        
        # Manipulacion de ERROR
        venta = get_object_or_404(Sale.objects.all(), pk=pk) 
        serializador = VentaReporteSerializer(venta)
        
        return(Response(serializador.data))
