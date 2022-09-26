from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from core.models import Card
from v2.serializers import CardListSerializer, CreateCardSerializer, CardDetailSerializer


class CardViewSet(ModelViewSet):
    '''A viewset for add/update/delete a card'''

    permission_classes = [IsAuthenticated,]
    lookup_field = 'token'

    def get_queryset(self):
        # return all cards of a user.
        return Card.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        # serialize data with appropriate serializers
        if self.action == "list":
            return CardListSerializer

        elif self.action == "create":
            return CreateCardSerializer

        elif self.action in ["update", "partial_update", "delete", "retrieve", "metadata"]:
            return CardDetailSerializer

    def get_serializer_context(self):
        return {"user" : self.request.user}

