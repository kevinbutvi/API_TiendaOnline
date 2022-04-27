from rest_framework import viewsets
from rest_framework.response import Response

from .models import Colours, Product
from .serializers import (ColorSerializer, PaginationSerializer, ProductSerializerViewSet)


class ColourViewSet(viewsets.ModelViewSet):
    """ CRUD para el modelo Colours """

    serializer_class = ColorSerializer
    queryset = Colours.objects.all() # Coleccion de datos con la que va a trabajar


class ProductViewSet(viewsets.ModelViewSet):
    """ Viewset para Producto """
    
    serializer_class = ProductSerializerViewSet
    queryset = Product.objects.all()
    pagination_class = PaginationSerializer


    def perform_create(self, serializer):
        """ Sobreescitura del PERFORME_CREATE para agregar URL de video Por Defecto """
        
        if not(serializer.validated_data["video"]):
            serializer.save(
                video="https://url_por_defecto.com"
            )
        else:
            serializer.save()
    
    def list(self, request, *args, **kwargs):
        """ Sobreescritura de LIST para mostrar lista personalizada """
        
        queryset = Product.objects.productos_por_user(self.request.user)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
