from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .models import Product
from .serializers import ProductSerializer



# Create your views here.

class ListProductUser(ListAPIView):
    """ Devuelve los productos filtrados por el usuario que lo creo """
    
    serializer_class = ProductSerializer
    
    authentication_classes = [TokenAuthentication] # Declara que tipo de Autenticacion que se utilizara
    permission_classes = [IsAuthenticated] # Define que tipos de autenticaciones permiten cargar la vista 
    
    def get_queryset(self):
        """ Sobreescitura del queryset para filtrar """
        
        usuario = self.request.user
        return (Product.objects.productos_por_user(usuario))


class ListProductStock(ListAPIView):
    """ Devuelve los productos que estan en Stock para usuarios autenticados 'por cualquier tipo de autenticacion' """
    
    serializer_class = ProductSerializer

    # A esta vista pueden acceder usuarios autenticados por cualquier medio. No es necesario que tengan Token
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Sobreescitura del queryset para filtrar """

        return (Product.objects.productos_por_stock())


class ListProducGenero(ListAPIView):
    """ Devuelve los productos por Genero """
    
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        """ Sobreescitura del queryset para filtrar """
        
        genero = self.kwargs['gender'] # Recupera el valor que se envia por parametro en la URL
        return (Product.objects.productos_por_genero(genero))


class FiltrarProductos(ListAPIView):
    """ Filtra segun paramentros enviados por url por METODO GET. Si es Hombre, Mujer o Unisex """
    
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        varon = self.request.query_params.get('man', None)
        mujer = self.request.query_params.get('woman', None)
        nombre = self.request.query_params.get('name', None)
        return (Product.objects.filtrar_productos(
            man = varon, 
            woman = mujer,
            name = nombre
        ))