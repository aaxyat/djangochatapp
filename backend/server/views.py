from django.db.models import Count
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response
from server import models
from server.schema import server_list_docs

from .serializer import ServerSerializer


class ServerListViewSet(viewsets.ViewSet):
    """
    # Server List API

    ## Description
    Viewset for listing servers with optional filtering.

    ## Query Parameters
    - **category** (str, optional): Filter servers by category name.
      - Example: `?category=gaming`
    - **qty** (int, optional): Limit the number of returned servers.
      - Example: `?qty=10`
    - **by_user** (bool, optional): Filter servers that the authenticated user is a member of.
      - Authentication required.
      - Example: `?by_user=true`
    - **by_serverid** (int, optional): Retrieve a specific server by ID.
      - Authentication required.
      - Example: `?by_serverid=42`
    - **with_num_members** (bool, optional): Include the count of members for each server.
      - Example: `?with_num_members=true`

    ## Responses
    - **200 OK**:
      Returns a list of servers matching the specified filters.
      ```json
      [
        {
          "id": 1,
          "name": "Gaming Server",
          "category": "gaming",
          "description": "A server for gamers",
          "num_members": 42  // Only included if with_num_members=true
        }
      ]
      ```
    - **401 Unauthorized**:
      Returned when authentication is required but the user is not authenticated.
    - **400 Bad Request**:
      Returned when the server ID is invalid or not found.
    """

    queryset = models.Server.objects.all()

    @server_list_docs
    def list(self, request):
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")
        by_user = request.query_params.get("by_user") == "true"
        by_serverid = request.query_params.get("by_serverid")
        with_num_members = request.query_params.get("with_num_members") == "true"

        if category:
            self.queryset = self.queryset.filter(category__name=category)

        if by_user:
            if request.user.is_authenticated:
                user_id = request.user.id
                self.queryset = self.queryset.filter(member=user_id)
            else:
                raise AuthenticationFailed("Authentication required.")
        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        if qty:
            self.queryset = self.queryset[: int(qty)]

        if by_serverid:
            if request.user.is_authenticated:
                try:
                    self.queryset = self.queryset.filter(id=by_serverid)
                    if not self.queryset.exists():
                        raise ValidationError(
                            f"Server with id {by_serverid} not found.",
                        )
                except ValueError:
                    raise ValidationError(f"Server value error {by_serverid}.")
            else:
                raise AuthenticationFailed("Authentication required.")

        serializer = ServerSerializer(
            self.queryset, many=True, context={"num_members": with_num_members}
        )
        return Response(serializer.data)
