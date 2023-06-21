import json

from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import authentication, generics, mixins, permissions

from .authentication import TokenAuthentication

from stat_track.models import Match, Player
from stat_track.permissions import IsStaffEditorPermission
from stat_track.serializers import MatchSerializer, PlayerSerializer


@api_view(["POST"])
def api_home(request, *args, **kwargs):
    """
    DRF API View
    """
    data = request.data
    serializer = PlayerSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        return Response(serializer.data)


class PlayerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    authentication_classes = [
        authentication.SessionAuthentication,
        TokenAuthentication
        ]
    permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]    # User permission authentication
    
player_list_create_view = PlayerListCreateAPIView.as_view()


class PlayerDetailAPIView(generics.RetrieveAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [permissions.DjangoModelPermissions]

player_detail_view = PlayerDetailAPIView.as_view()


class PlayerUpdateAPIView(generics.UpdateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.DjangoModelPermissions]

    def perform_update(self, serializer):
        instance = serializer.save()

player_update_view = PlayerUpdateAPIView.as_view()


class PlayerDestroyAPIView(generics.DestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.DjangoModelPermissions]

    def perform_destroy(self, instance):
        super().perform_destroy(instance)

player_delete_view = PlayerDestroyAPIView.as_view()


class PlayerMixinView(
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView
    ):

    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    lookup_field = 'pk'

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):    #HTTP -> get
        pk = kwargs.get("pk")
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    # def post()

player_mixin_view = PlayerMixinView.as_view()

# One view to handle CREATE, LIST and DETAIL             # NOT IN USE
@api_view(['GET', 'POST'])
def player_alt_view(request, pk=None, *args, **kwargs):
    method = request.method

    if method == "GET":
        if pk is not None:
            # detail view
            obj = get_object_or_404(Player, pk=pk)
            data = PlayerSerializer(obj, many=False).data
            return Response(data)

        # list view
        queryset = Player.objects.all()
        data = PlayerSerializer(queryset, many=True).data
        return Response(data)

    if method == "POST":
        #create an item
        serializer = PlayerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            first_name = serializer.validated_data.get('first_name')
            last_name = serializer.validated_data.get('last_name')

            if Player.objects.filter(first_name=first_name, last_name=last_name).exists():
                return Response({"invalid": "Player already exists"})
            return Response(serializer.data)
        return Response({"invalid": "not good data"}, status=400)