# from django.shortcuts import render
from django.db.models import Count
from rest_framework import status, viewsets
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from .models import server
from .schema import server_list_docs
from .serializer import serverSerializer


class ServerListViewSet(viewsets.ViewSet):

    queryset = server.objects.all()
    print(queryset)

    @server_list_docs
    def list(self, request):
        """
        List all server instances with optional filtering.

        The following query parameters can be used to filter the results:

        - catagory: Filter servers by category name.
        - qty: Limit the number of returned servers.
        - by_user: If true, filter the servers to those associated with the authenticated user.
        - by_server_id: Filter the results to a specific server by its ID.
        - with_num_members: If true, include the number of members associated with each server in the response.

        Args:
            request (Request): The HTTP request object containing query parameters.

        Returns:
            Response: A Response object containing the serialized data of the filtered server instances,
                      or an error response if authentication fails, a server is not found, or
                      if there is a ValueError in processing the request.

        Raises:
            AuthenticationFailed: If the user is not authenticated and attempts to filter by user
                                  or by server ID.
        """

        catagory = request.query_params.get("catagory")
        qty = request.query_params.get("qty")
        by_user = request.query_params.get("by_user") == "true"
        by_server_id = request.query_params.get("by_server_id")
        with_num_members = request.query_params.get("with_num_members") == "true"

        if (by_user or by_server_id) and not request.user.is_authenticated:
            raise AuthenticationFailed()

        if catagory:
            self.queryset = self.queryset.filter(catagory__name=catagory)
        if by_user:
            user_id = request.user.id
            self.queryset = self.queryset.filter(member=user_id)
        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count("member"))
        if qty:
            self.queryset = self.queryset[: int(qty)]
        if by_server_id:
            try:
                self.queryset = self.queryset.filter(id=by_server_id)
                if not self.queryset.exists():
                    return Response(status=status.HTTP_404_NOT_FOUND)
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serverSerializer(
            self.queryset, many=True, context={"num_members": with_num_members}
        )
        return Response(serializer.data)
