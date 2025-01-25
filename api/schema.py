from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

from .serializer import channelSerializer, serverSerializer

server_list_docs = extend_schema(
    responses=serverSerializer(many=True),
    parameters=[
        OpenApiParameter(
            name="catagory",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="catagory of servers to retrieve",
        ),
        OpenApiParameter(
            name="qty",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="number of servers to retrieve",
        ),
        OpenApiParameter(
            name="by_user",
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="filter server by authenticated user",
        ),
        OpenApiParameter(
            name="with_num_members",
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="include the number of members for each server in the response",
        ),
        OpenApiParameter(
            name="by_server_id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="filter by the id of the server",
        ),
    ],
)
