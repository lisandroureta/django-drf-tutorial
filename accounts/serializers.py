from rest_framework import serializers
from django.contrib.auth.models import User
from snippets.models import Snippet # Necesitamos importar el modelo Snippet aquí

class UserSerializer(serializers.HyperlinkedModelSerializer):
    # Fíjate que referenciamos la vista 'snippet-detail' que vive en la otra app
    snippets = serializers.HyperlinkedRelatedField(
        many=True, 
        view_name='snippet-detail', 
        read_only=True
    )

    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'snippets', 'followers_count', 'following_count']

    def get_followers_count(self, obj):
        # Accedemos al perfil y contamos cuántos lo tienen en su lista 'following'
        # Nota: 'followers' es el related_name que definimos en el modelo Profile
        return obj.followers.count()

    def get_following_count(self, obj):
        # Accedemos al perfil del usuario y contamos a cuántos sigue
        return obj.profile.following.count()

class RegisterSerializer(serializers.ModelSerializer):
    # Definimos los campos que queremos pedirle al usuario
    email = serializers.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        # IMPORTANTE: La contraseña solo se escribe, nunca se devuelve en la respuesta
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # Sobrescribimos el método create para usar 'create_user'
        # Esto asegura que la contraseña se encripte (hash)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user