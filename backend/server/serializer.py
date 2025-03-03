from rest_framework import serializers
from server import models


class ChannelSerializer(serializers.ModelSerializer):
    """A serializer class for the Channel model.

    This serializer converts Channel model instances to JSON format and vice versa,
    including all fields from the Channel model.

    Attributes:
        Meta: Inner class defining metadata for the serializer
            - model: The Channel model to be serialized
            - fields: All fields from the model are included in serialization
    """

    class Meta:
        model = models.Channel
        fields = "__all__"


class ServerSerializer(serializers.ModelSerializer):
    """
    A serializer for the Server model that handles server-related data serialization.

    This serializer includes the number of members and associated channels for a server.
    It excludes the 'member' field from serialization.

    Attributes:
        num_members (SerializerMethodField): A method field that returns the number of
        server members
        channel_server (ChannelSerializer): Nested serializer for related channels with
        many=True relationship

    Methods:
        get_num_members(obj): Returns the number of members if the attribute exists
        to_representation(instance): Customizes the serialized representation by handling
        num_members field

    Example:
        ```
        serializer = ServerSerializer(server_instance)
        serialized_data = serializer.data
        ```
    """

    num_members = serializers.SerializerMethodField()
    channel_server = ChannelSerializer(many=True)

    class Meta:
        model = models.Server
        exclude = ["member"]

    def get_num_members(self, obj):
        if hasattr(obj, "num_members"):
            return obj.num_members
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        num_members = self.context.get("num_members")
        if not num_members:
            data.pop("num_members")
        return data
