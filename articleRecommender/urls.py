from . import views
from django.urls import path


urlpatterns = [
    path('home/',views.home),
    path('article/',views.ArticleView.as_view(),name='article'),
    path('article/<int:pk>/',views.ArticleView.as_view()),
    ]
