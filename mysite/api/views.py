import json

from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics

from stat_track.models import Match, Player
from stat_track.serializers import MatchSerializer, PlayerSerializer

@api_view(["POST"])
def api_home(request, *args, **kwargs):
    """
    DRF API View
    """
    data = request.data
    serializer = PlayerSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):

        print(serializer.data)
        return Response(serializer.data)


class PlayerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    
player_list_create_view = PlayerListCreateAPIView.as_view()


class PlayerDetailAPIView(generics.RetrieveAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

player_detail_view = PlayerDetailAPIView.as_view()


# class PlayerListAPIView(generics.ListAPIView):
#     queryset = Player.objects.all()
#     serializer_class = PlayerSerializer

# player_detail_view = PlayerListAPIView.as_view()


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