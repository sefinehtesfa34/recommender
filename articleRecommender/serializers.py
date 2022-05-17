
from rest_framework import serializers
from .models import Article,Interactions#RecommendationConfiguration
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Article
        fields='__all__'

class InteractionsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Interactions
        fields='__all__'
class ArticleIdSerializer(serializers.ModelSerializer):
    class Meta:
        model=Interactions
        fields=['contentId']

class ContentIdSerializer(serializers.ModelSerializer):
    class Meta:
        model=Article
        fields=['contentId']
        







