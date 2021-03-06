from rest_framework import generics
from rest_framework.authentication import (SessionAuthentication,
                                           BasicAuthentication)
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer, \
    SnippetSimpleSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly

"""
http http://127.0.0.1:8000/snippets/
http -a admin:adminadmin POST http://127.0.0.1:8000/snippets/ code="print(789)"

http http://127.0.0.1:8000/snippets/2/
http POST http://127.0.0.1:8000/snippets/ code="public class Name { }"
"""


class SnippetList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication]
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly,
    #                       permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Obtiene una lista de Snippets: get  http://127.0.0.1:8008/snippets/
        [{"owner":"admin","owner_id":1,"id":1,"title":"","code":"print(111)","linenos":true,"language":"python","style":"friendly"},{"owner":"admin","owner_id":1,"id":2,"title":"","code":"print(222)","linenos":false,"language":"python","style":"friendly"}]
        :param request: 
        :param format: 
        :return: 
        """
        snippets = Snippet.objects.all()
        serializer = SnippetSimpleSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        post http://127.0.0.1:8008/snippets/
         {
            "title": "",
            "code": "print(456)",
            "linenos": false,
            "language": "python",
            "style": "friendly"
        }
        :param request: 
        :param format: 
        :return: 
        """
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.update(instance=snippets, validated_data=serializer.validated_data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        
        :param request: 
        :param pk: 
        :param format: 
        :return: 
        """
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
