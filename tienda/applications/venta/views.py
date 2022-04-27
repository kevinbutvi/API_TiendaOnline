from django.shortcuts import render
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Product, Sale, SaleDetail
from .serializers import ProcesoVentaSerializer, VentaReporteSerializer

# Create your views here.

class ReporteVentasList(ListAPIView):
    """ Reporte de ventas con detalle """
    
    serializer_class = VentaReporteSerializer
    
    def get_queryset(self):
        
        return (Sale.objects.all())


class RegistrarVenta(CreateAPIView):
    """ Vista para la creacion de una nueva venta. Requiere Autenticacion por Token """
    
    serializer_class = ProcesoVentaSerializer
    
    authentication_classes = [TokenAuthentication] # Tipo de Autenticacion 
    permission_classes = [IsAuthenticated] # Permisos
    
    def create(self, request, *args, **kwargs):
        """ Sobreescritura de CREATE para hacer almacenamiento en DB """
        
        datos = request.data
        serializador = ProcesoVentaSerializer(data=datos) # DESERIALIZA los datos recibidos
        serializador.is_valid(raise_exception = True)
        
        # Datos validados
        tipo_recibo = serializador.validated_data["type_invoce"]
        tipo_pago = serializador.validated_data["type_payment"]
        direcccion = serializador.validated_data["address_send"]
        
        # Recupero los productos de la venta
        productos = Product.objects.filter(
            id__in = serializador.validated_data["productos"]
        ) # Devuelve TODOS los productos que coincidan el ID de la tabla con el ID que se pasa en el arrya del serializador. Todos los que coinciden quedan almacenados en la variable 'productos'
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
        
        ventas_detalle = [] # Variable que se utilizara para almacenar todos los detalles de ventas y para BULK_CREATE
        
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