from rest_framework import serializers

from .models import channel, server


class channelSerializer(serializers.ModelSerializer):
    class Meta:
        model = channel
        fields = "__all__"


class serverSerializer(serializers.ModelSerializer):
    num_members = serializers.SerializerMethodField()
    channel_server = channelSerializer(many=True)

    class Meta:
        model = server
        exclude = ("member",)

    def get_num_members(self, obj):
        if hasattr(obj, "num_members"):
            return obj.num_members
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        num_members = self.context.get("num_members")
        if not num_members:
            data.pop("num_members", None)
        return data
