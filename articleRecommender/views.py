from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from articleRecommender.evaluatorModel import ModelEvaluator

from articleRecommender.models import Article, Interactions
from articleRecommender.preProcessorModel import PreprocessingModel
from .serializers import  ArticleSerializer, InteractionsSerializer 


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
    def __init__(self):
        
        self.interactions=Interactions.objects.filter()
        self.article=Article.objects.filter()
        
        self.user_interacted=None
        self.interactions_serializer=InteractionsSerializer(self.interactions,many=True)
        self.article_serializer=ArticleSerializer(self.article,many=True) 
        self.eventStrength={
            "LIKE":1.0,
            "VIEW":5.0,
            "FOLLOW":2.0,
            "UNFOLLOW":2.0,
            "DISLIKE":1.0,
            "REACT-POSITIVE":1.5,
            "REACT-NEGATIVE":1.5,
            "COMMENT-BEST-POSITIVE":3.0,
            "COMMENT-AVERAGE-POSITIVE":2.5,
            "COMMENT-GOOD-POSITIVE":2.0,
            "COMMENT-BEST-NEGATIVE":3.0,
            "COMMENT-AVERAGE-NEGATIVE":2.5,
            "COMMENT-GOOD-NEGATIVE":2.0,    
            }
        self.preprocessingModel=PreprocessingModel(self.interactions_serializer.data,self.article_serializer.data,self.eventStrength)
        
        
    def get_object(self,userId):
        try:
            return Interactions.objects.filter(userId=userId)
            
        except Interactions.DoesNotExist:
            return None 
    
    def get(self,request,userId,format=None):
        
        user_interact_contentId=self.get_object(userId)
        try:
            assert(user_interact_contentId)
        except AssertionError:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        self.preprocessingModel.getUserId(userId)
        self.recommended_items=self.preprocessingModel.recommended
        train,test=self.preprocessingModel.trainTestSpliter()
        full_set=self.preprocessingModel.interactions_full_indexed_df
        articles_df=self.preprocessingModel.article_df
        
        self.modelEvaluator=ModelEvaluator(train,test,full_set,articles_df)
    
        serializer=InteractionsSerializer(user_interact_contentId,many=True)
        self.user_interacted=serializer.data
        
        return Response(self.recommended_items)
        
        
        
        
        












