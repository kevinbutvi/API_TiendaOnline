from rest_framework import pagination, serializers

from .models import Colours, Product


class ColorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Colours
        fields = (
            'colour',
        )


class ProductSerializer(serializers.ModelSerializer):

    colours = ColorSerializer(many=True)
    
    class Meta:
        model = Product
        fields = (
            'name',
            'description',
            'man',
            'woman',
            'weight',
            'price_purchase',
            'price_sale',
            'main_image',
            'image1',
            'image2',
            'image3',
            'image4',
            'colours',
            'video',
            'stock',
            'num_sales',
            'user_created',
        )


class PaginationSerializer(pagination.PageNumberPagination):
    """ Paginador """
    
    page_size = 5
    max_page_size = 50



class ProductSerializerViewSet(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('__all__')
