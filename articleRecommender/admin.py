from django.contrib import admin

from articleRecommender.models import Interactions,Article,RecommendationConfiguration

admin.site.register(Interactions)
admin.site.register(Article)
admin.site.register(RecommendationConfiguration)
