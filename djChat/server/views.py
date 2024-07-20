from rest_framework.exceptions import ValidationError, AuthenticationFailed
from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.response import Response
from django.db.models import Count
# Create your views here.
class ServerListViewSet(viewsets.ViewSet):

    queryset = Server.objects.all()
    def list(self, request):
        with_num_members = request.query_params.get('with_num_members') == True
        by_serverid = request.query_params.get('by_serverid')
        by_user= request.query_params.get("by_user") == 'true'

        if by_user or by_serverid and not request.user.is_authenticated:
            raise AuthenticationFailed()
        
        if qty := request.query_params.get("qty"):
            self.queryset = self.queryset[:int(qty)]

        if with_num_members:
            self.queryset = self.queryset.annotate(num_members = Count('member'))

        if category := request.query_params.get("category"):
            self.queryset.filter(category = category)

        if by_serverid:
            try:
                self.queryset.filter(id = by_serverid)
                if not self.queryset.exists():
                    raise ValueError(detail = f'Server with id {by_serverid} not found')
            except ValueError as e:
                raise ValidationError(
                    detail=f'Server with id {by_serverid} not found'
                ) from e


        serializer = ServerSerializer(self.queryset, many=True)
        return Response(serializer.data)


