from django.db import models

class Article(models.Model):
    authorId=models.CharField(max_length=100)
    authorResidence=models.CharField(max_length=100)
    communtId=models.CharField(max_length=100)
    content=models.TextField()
    contentId=models.CharField(max_length=100)
    source=models.CharField(max_length=100)
    timestamp=models.IntegerField() 
    title=models.CharField(max_length=100)
    
class Interactions(models.Model):
    userId=models.CharField(max_length=100,unique=True)
    location=models.CharField(max_length=100)
    eventType=models.IntegerField(unique=True)
    articleId=models.ForeignKey(Article,on_delete=models.CASCADE)
    communityId=models.CharField(max_length=100)
    source=models.IntegerField()
    timestamp=models.IntegerField()
    

class RecommendationConfiguration(models.Model):
    communityId=models.UUIDField(max_length=100)
    highQuality=models.FloatField()
    content=models.TextField()
    pattern=models.FloatField()
    popularity=models.FloatField()
    random=models.FloatField() 
    timelines=models.FloatField()
    
    
    
    