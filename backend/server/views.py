from rest_framework import viewsets
from rest_framework.response import Response
from server import models

from .serializer import ServerSerializer


class ServerListViewSet(viewsets.ViewSet):
    queryset = models.Server.objects.all()

    def list(self, request):
        category = request.query_params.get("category")
        if category:
            self.queryset = self.queryset.filter(category=category)

        serializer = ServerSerializer(self.queryset, many=True)
        return Response(serializer.data)
