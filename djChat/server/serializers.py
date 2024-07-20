from rest_framework import serializers
from .models import *
class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = '__all__'
class ServerSerializer(serializers.ModelSerializer):
    num_members = serializers.SerializerMethodField()
    channel_server = ChannelSerializer(many = True)
    class Meta:
        model = Server
        exclude = ('member',)