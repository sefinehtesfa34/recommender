from . import views
from django.urls import path


urlpatterns = [
    path('article/',views.ArticleView.as_view(),name='article'),
    path('article/<int:authorId>/',views.ArticleView.as_view()),
    path('interact/',views.InteractionsView.as_view()),
    path('interact/<int:userId>/',views.InteractionsView.as_view()),
    path('recommend/<int:userId>/',views.PopularityRecommenderView.as_view()),
    path('content-based/<int:userId>/',views.ContentBasedRecommenderView.as_view()),
    
    ]
