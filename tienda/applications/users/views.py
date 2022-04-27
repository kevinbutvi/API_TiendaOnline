from django.shortcuts import render
from django.views.generic import TemplateView
from firebase_admin import auth
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import LoginSocialSerializer


# Create your views here.

class LoginUser(TemplateView):
    template_name = "users/login.html"


class GoogleLoginView(APIView):
    serializer_class = LoginSocialSerializer

    def post(self, request):
        """ Sobreescritura de Post para creacion de usuario y token personalizado """

        serializer = LoginSocialSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        id_token = serializer.data.get('token_id')
        decoded_token = auth.verify_id_token(id_token)
        email = decoded_token['email']
        name = decoded_token['name']

        usuario, created = User.objects.get_or_create(
            email=email,
            defaults={
                'full_name': name,
                'email': email,
                'is_active': True
            }
        )
        
        if created:
            # creamos el token
            token = Token.objects.create(user=usuario)
        else:
            # Creamos el nuevo usuario
            token = Token.objects.get(user=usuario)
        
        userGet = {
            'id': usuario.pk,
            'email': usuario.email,
            'full_name': usuario.full_name,
            'genero': usuario.genero,
            'date_birth': usuario.date_birth,
            'city': usuario.city
        }
        return Response({
            'token': token.key,
            'user': userGet
        })
