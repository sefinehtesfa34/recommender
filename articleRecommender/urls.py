from . import views
from django.urls import path


urlpatterns = [
    path('article/',views.ArticleView.as_view(),name='article'),
    path('article/<int:pk>/',views.ArticleView.as_view()),
    path('interact/',views.InteractionsView.as_view()),
    path('interact/<int:pk>/',views.InteractionsView.as_view()),
    path('recommend/<int:userId>/',views.RecommenderView.as_view()),
    ]
