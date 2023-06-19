import json

from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.response import Response

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
