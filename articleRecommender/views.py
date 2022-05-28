from rest_framework.pagination import PageNumberPagination
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from articleRecommender.content_based.content_based_recommender import ContentBasedRecommenderModel
from articleRecommender.model_evaluator.evaluatorModel import ModelEvaluator
from articleRecommender.models import Article, Interactions
from articleRecommender.data_preprocessor.preProcessorModel import PreprocessingModel
from .serializers import  ArticleSerializer, ContentIdSerializer, InteractionsSerializer 


class ArticleView(APIView,PageNumberPagination):
    def get_object(self,authorId):
        try:
            return Article.objects.filter(authorId=authorId)
        except Article.DoesNotExist:
            return Http404
    
    def get(self,request,authorId=None,format=None):
        if authorId:
            article=self.get_object(authorId)
            if article is not Http404:
                result=self.paginate_queryset(article,request,view=self)
                
                serializer=ArticleSerializer(result,many=True)
                return self.get_paginated_response(serializer.data)
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        article=Article.objects.all()
        result=self.paginate_queryset(article,request,view=self)
        serializer=ArticleSerializer(result,many=True)    
        return self.get_paginated_response(serializer.data)
    
    
    def post(self,request,format=None):
        serializer=ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,authorId,format=None):
        article=self.get_object(authorId)
        serializer=ArticleSerializer(article,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, authorId, format=None):
        snippet = self.get_object(authorId)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

                
            
class InteractionsView(APIView,PageNumberPagination):
    def get_object(self,userId):
        try:
            return Interactions.objects.filter(userId=userId)
        except Interactions.DoesNotExist:
            return Http404
    
    def post(self,request,format=None):
        serializer=InteractionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,userId,format=None):
        article=self.get_object(userId)
        serializer=InteractionsSerializer(article,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, userId, format=None):
        snippet = self.get_object(userId)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    def get(self,request,userId=None,format=None):
        if userId:
            article=self.get_object(userId)
            if article is not Http404:
                result=self.paginate_queryset(article,request,view=self)
                serializer=InteractionsSerializer(result,many=True)
                return self.get_paginated_response(serializer.data)
            return Response(status=status.HTTP_404_NOT_FOUND)
        article=Interactions.objects.all()
        result=self.paginate_queryset(article,request,view=self)
        serializer=InteractionsSerializer(result,many=True)    
        
        return self.get_paginated_response(serializer.data)
    
        
    def post(self,request,format=None):
        serializer=InteractionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,userId,format=None):
        article=self.get_object(userId)
        serializer=InteractionsSerializer(article,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,userId,format=None):
        article=self.get_object(userId)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
 
class PopularityRecommenderView(APIView,PageNumberPagination):
    def __init__(self):
        
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
        
    def get_object(self,userId):
        self.excluded_article=Interactions.objects.filter(userId=userId).only("contentId")
        serializer=ContentIdSerializer(self.excluded_article,many=True)
        self.excluded_article_set=set()
        for dict in serializer.data:
            self.excluded_article_set.add(list(dict.values())[0])
        
        
        try:
            return Interactions.objects.filter(userId=userId)
            
        except Interactions.DoesNotExist:
            return None 
    
    def get(self,request,userId,format=None):
        
        user_interact_contentId=self.get_object(userId)
        
        self.interactions=Interactions.objects.exclude(contentId__in=self.excluded_article_set)
        self.article=Article.objects.exclude(pk__in=self.excluded_article_set)
        self.user_interacted=None
        self.interactions_serializer=InteractionsSerializer(self.interactions,many=True)
        self.article_serializer=ArticleSerializer(self.article,many=True) 
        self.preprocessingModel=PreprocessingModel(self.interactions_serializer.data,self.article_serializer.data,self.eventStrength,flag="popularity")    
        try:
            assert(user_interact_contentId)
        except AssertionError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
            
        self.recommended_items=self.preprocessingModel.getUserIdAndRecommend(userId)
        
        train,test=self.preprocessingModel.trainTestSpliter()
        full_set=self.preprocessingModel.interactions_full_indexed_df
        articles_df=self.preprocessingModel.article_df
        self.modelEvaluator=ModelEvaluator(train,test,full_set,articles_df)
        serializer=InteractionsSerializer(user_interact_contentId,many=True)
        self.user_interacted=serializer.data
        
        recommended_articles=Article.objects.filter(pk__in=list(self.recommended_items))
        
        result=self.paginate_queryset(recommended_articles,request,view=self)
        serializer=ArticleSerializer(result,many=True)    
        
        
        return self.get_paginated_response(serializer.data)

class ContentBasedRecommenderView(APIView):
    def __init__(self):
        self.interactions=Interactions.objects.all()
        self.article=Article.objects.all()
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
        self.preprocessingModel=PreprocessingModel(\
                self.interactions_serializer.data,\
                self.article_serializer.data,\
                self.eventStrength,flag="content-based")
        
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
            
        self.recommended_items=self.preprocessingModel.getUserIdAndRecommend(userId)
        
        train,test=self.preprocessingModel.trainTestSpliter()
        full_set=self.preprocessingModel.interactions_full_indexed_df
        articles_df=self.preprocessingModel.article_df
        self.modelEvaluator=ModelEvaluator(train,test,full_set,articles_df)
        serializer=InteractionsSerializer(user_interact_contentId,many=True)
        self.user_interacted=serializer.data


        result=self.paginate_queryset(self.recommended_items,request,view=self)
        serializer=ArticleSerializer(result,many=True)    
        
        
        return self.get_paginated_response(serializer.data)
        
        
        
