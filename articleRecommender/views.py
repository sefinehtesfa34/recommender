from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from articleRecommender.models import Article, Interactions
from articleRecommender.serializers import ArticleSerializer, InteractionsSerializer 

class ArticleView(APIView):
    def get_object(self,pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Http404
    
    def get(self,request,pk=None,format=None):
        if pk:
            article=self.get_object(pk)
            if article is not Http404:
                serializer=ArticleSerializer(article)
                return Response(serializer.data)
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        article=Article.objects.all()
        serializer=ArticleSerializer(article,many=True)
        return Response(serializer.data)
    
    def post(self,request,format=None):
        serializer=ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,pk,format=None):
        article=self.get_object(pk)
        serializer=ArticleSerializer(article,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

                
            
class InteractionsView(APIView):
    def get_object(self,pk):
        try:
            return Interactions.objects.get(pk=pk)
        except Interactions.DoesNotExist:
            return Http404
    
    def get(self,request,pk=None,format=None):
        if pk:
            article=self.get_object(pk)
            if article is not Http404:
                serializer=InteractionsSerializer(article)
                return Response(serializer.data)
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        article=Interactions.objects.all()
        serializer=InteractionsSerializer(article,many=True)
        return Response(serializer.data)
    
    def post(self,request,format=None):
        serializer=InteractionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,pk,format=None):
        article=self.get_object(pk)
        serializer=InteractionsSerializer(article,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk,format=None):
        article=self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
 
class RecommenderView(APIView):
    
    def get_object(self,userId):
        try:
            return Interactions.objects.get(userId=userId)
        except Interactions.DoesNotExist:
            return Http404
    
    def get(self,request,userId,format=None):
        
        article=self.get_object(userId)
        serializer=InteractionsSerializer(article)
        if article is not Http404:
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)
        
        
        












