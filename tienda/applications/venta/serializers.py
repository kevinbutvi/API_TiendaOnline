from rest_framework import serializers
from .models import Sale, SaleDetail



class VentaReporteSerializer(serializers.ModelSerializer):
    """ Reporte con detalles de ventas """
    
    producto = serializers.SerializerMethodField() # Campo Producto Personalizado
    
    class Meta:
        model = Sale
        fields = (
            'id',
            'date_sale',
            'amount',
            'count',
            'type_invoce',
            'cancelado',
            'type_payment',
            'state',
            'address_send',
            'anulate',
            'user',
            'producto',
        )
    
    def get_producto(self, obj):
        """ Definicion para 'producto' """
        
        consulta = SaleDetail.objects.Detalle_producto_ventas(obj.id) 
        consulta_serializada = DetalleVentaProductoSerializer(consulta, many=True).data # Serializacion de 'consulta' + acceso a datos
        
        return (consulta_serializada)


class DetalleVentaProductoSerializer(serializers.ModelSerializer):
    """ Serializador para el modelo SaleDetail """
    
    class Meta:
        model = SaleDetail
        fields = (
            'id',
            'sale',
            'product',
            'count',
            'price_purchase',
            'price_sale',
        )


class ProductDetailSerializer(serializers.Serializer):
    """ Serializador para PROCESO DE VENTA """
    
    pk = serializers.IntegerField()
    count = serializers.IntegerField()


class ArrayIntegerSerializer(serializers.ListField):
    """ Serializador para proceso de Venta. Envia Array con todos los ID de productos """

    child = serializers.IntegerField() # Tipo de datos que se envian en el arreglo



class ProcesoVentaSerializer(serializers.Serializer):
    """ Serializador personalizado para proceso de Venta. RECIBE UN LISTFIEL SERIALIZER (array) """
    
    type_invoce = serializers.CharField()
    type_payment = serializers.CharField()
    address_send = serializers.CharField()
    productos = ArrayIntegerSerializer()
    cantidades = ArrayIntegerSerializer()
    
    def validate(self, data):
        """ Validacion GENERAL por acceso desde 'data' """
    
        if data["type_payment"] not in ('0', '1', '2'):
            raise serializers.ValidationError("El valor para Type_Payment es erroneo")
        
        return(data)

    
    def validate_type_invoce(self, value):
        """ Se personalizada para cada serilizador """
        
        if value not in ('0', '3', '4'):
            raise serializers.ValidationError("El valor para Type_Invoce es erroneo")
        
        return (value)