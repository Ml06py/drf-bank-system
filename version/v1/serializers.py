from  rest_framework import  serializers
from django.contrib.auth.models import User
from v1.models import Card

class RegisterUserSerializer(serializers.ModelSerializer):
    '''
        Create User serializer
    '''
    class Meta:
        model = User
        fields = ('id','first_name', 'last_name', 'email', 'password')

        extra_kwargs = {'password': {'write_only': True},}

        def create(self, validated_data):
            '''
                Create user with serializer data
            '''
            user = User.objects.create_user(**validated_data)
            return user

class CreateCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ("password",)
        extra_kwargs = {'password': {'write_only': True},}

class ListCardSerializer(serializers.ModelSerializer):
    '''List of users cards.'''
    class Meta:
        model = Card
        fields = ("number", "token")

class DetailCardSerializer(serializers.ModelSerializer):
    '''
        Return extra detail about a card
    '''
    owner = serializers.CharField(source="owner.email")
    class Meta:
        model = Card
        fields = ("owner", "number", "cvv", "balance", "date_created", "token")