from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from app.api.serializers import PlantedTreeSerializer
from app.models import PlantedTree


class PlantedTreesViewSet(ListAPIView):
    serializer_class = PlantedTreeSerializer
    queryset = PlantedTree.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query_set = PlantedTree.objects.filter(user=self.request.user)
        return query_set
