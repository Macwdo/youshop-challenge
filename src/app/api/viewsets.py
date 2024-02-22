from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from app.api.serializers import PlantedTreeSerializer
from app.models import PlantedTree


class PlantedTreesViewSet(ListAPIView):
    serializer_class = PlantedTreeSerializer
    queryset = PlantedTree.objects.all()
    permission_classes = [IsAuthenticated]

    # type: ignore
    def get_queryset(self) -> list[PlantedTree]:
        return PlantedTree.objects.filter(user=self.request.user)
