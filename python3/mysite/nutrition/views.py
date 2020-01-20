from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext

from django.template import Context, Template

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save


from django.contrib.auth import get_user_model

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

        
import datetime
def set_cookie(response, key, value, max_age):
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires)

def index(request):
    print(request.user)
    try:
        token = Token.objects.get(user=request.user)
    except:
        token = ''
    response = render_to_response( 'public/index.html', 
                              context_instance=RequestContext(request))
    set_cookie(response, 'token', token, 3*24*60*60)
    set_cookie(response, 'username', request.user.username, 3*24*60*60)
    set_cookie(response, 'id', request.user.id, 3*24*60*60)
    return response




from rest_framework.response import Response
from rest_framework.decorators import api_view
import asyncio

import threading



from nutrition.models import *
from nutrition.serializers import ItemSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from nutrition.permissions import IsOwnerOrReadOnly


class ItemList(APIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                  IsOwnerOrReadOnly,)
    def get(self, request, format=None):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemDetail(APIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                  IsOwnerOrReadOnly,)
    def get_object(self, pk):
        try:
            return Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework import generics

class AddCommentList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class AddCommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)