from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.shortcuts import get_object_or_404
from .serializers import (RegisterUserSerializer,
                          CreateCardSerializer, ListCardSerializer, DetailCardSerializer, ChangePasswordCardSerializer,
                          TransactionSerializer, TransactionListSerializer)
from v1.models import Card, User, Transaction


class RegisterUserApi(APIView):
    '''
        Register a user with given information
    '''
    serializer_class = RegisterUserSerializer

    def post(self, request):
        ser_data = self.serializer_class(data=request.data)
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data)
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class CardCreateApi(generics.CreateAPIView):
    '''
        Create A new Card
    '''
    permission_classes = [IsAuthenticated,]
    serializer_class = CreateCardSerializer

    def perform_create(self, serializer):
            serializer =  serializer.save(owner=self.request.user)
            return Response(serializer, status=status.HTTP_201_CREATED)


class CardListApi(generics.ListAPIView):
    '''
        Return list of users cards
    '''
    permission_classes = [IsAuthenticated,]
    serializer_class = ListCardSerializer

    def get_queryset(self):
        return Card.objects.filter(owner = self.request.user)


class CardDetailApi(generics.RetrieveAPIView):
    '''
        Return detail of a card such as balance;
        only owner of a card can access this page.
    '''
    queryset = Card.objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = DetailCardSerializer

    def get_object(self):
        return get_object_or_404(Card ,token= self.kwargs["token"],
                                   owner= self.request.user)

class CardPasswordUpdate(APIView):
    '''
        Owner of a card can change one of cards password.
    '''
    permission_classes = [IsAuthenticated,]
    serializer_class = ChangePasswordCardSerializer

    def put(self, request, token):
        ser_data = self.serializer_class(data=request.data)
        object = get_object_or_404(Card, token= token, owner= self.request.user)

        if ser_data.is_valid():
            if ser_data.validated_data["old_password"] == ser_data.validated_data['new_password']:
                return Response({"failed" : "Passwords must not be same"}, status=status.HTTP_400_BAD_REQUEST)
            if ser_data.validated_data["old_password"] == object.password:
                object.password = ser_data.validated_data['new_password']
                object.save()
                return Response({"success":"password changed"}, status=status.HTTP_201_CREATED)
            return Response({"failed" : "Your old password is wrong"}, status=status.HTTP_400_BAD_REQUEST)


class CardTransactionApi(APIView):
    '''
        Create a Transaction and transfer money to other card.
    '''
    permission_classes = [IsAuthenticated,]
    serializer_class = TransactionSerializer

    def post(self, request):
        ser_data = self.serializer_class(data=request.data)
        if ser_data.is_valid():
            Transaction.objects.create(
                card_model=Card, user=self.request.user,
                from_card=ser_data.validated_data["from_card"],
                cvv=ser_data.validated_data["cvv"],
                password=ser_data.validated_data["password"],
                to_card=ser_data.validated_data["to_card"],
                amount=ser_data.validated_data["amount"]
            )

            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionListApi(generics.ListAPIView):
    '''
        Show 10 latest transactions of a card (only available for owners)
    '''
    permission_classes = [IsAuthenticated,]
    serializer_class = TransactionListSerializer

    def get_queryset(self):
        card = get_object_or_404(Card, owner=self.request.user, number= self.kwargs["c_number"])
        object = card.transactions.all()[:10]
        return object
