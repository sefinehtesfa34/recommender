
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




