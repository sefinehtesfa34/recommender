import pandas as pd
from sklearn.model_selection import train_test_split
import math
from articleRecommender.content_based.content_based_recommender import ContentBasedRecommenderModel 

from articleRecommender.popularity_recommender.recommender import PopularityRecommender
class PreprocessingModel:
    def __init__(self,interactions_json,article_json,eventStrength,flag=None):
        self.interaction_json=interactions_json
        self.article_json=article_json
        self.eventStrength=eventStrength
        self.interactions_df=pd.DataFrame(self.interaction_json)
        self.article_df=pd.DataFrame(self.article_json)
        print(self.interactions_df.columns)
        self.preporcessor()
        self.recommended=None
        self.flag=flag
        if self.flag=="popularity":
            self.popularity_model=PopularityRecommender(self.interactions_df,self.article_df)
        if self.flag=="content-based":
            self.contentBasedRecommenderModel=ContentBasedRecommenderModel(self.article_df,self.interactions_df)
        
        
    def getUserIdAndRecommend(self,userId):
        if self.flag=='popularity':
            recommended_items=self.popularity_model.recommend_items(userId)
            
        if self.flag=="content-based":
            recommended_items=self.contentBasedRecommenderModel.recommend_with_userId(userId)
        return recommended_items 
    def preporcessor(self):
        self.interactions_df['eventStrength'] = self.interactions_df['eventType'].apply(lambda x: self.eventStrength.get(x,0))
        def smooth_user_preference(x):
            return math.log(1+x, 2)
    
        
        self.interactions_df = self.interactions_df \
                    .groupby(['userId', 'contentId'])['eventStrength'].sum().apply(smooth_user_preference).reset_index()
        
    def trainTestSpliter(self):
        interactions_train_df, interactions_test_df = train_test_split(self.interactions_df,
                                 
                                   test_size=0.20,
                                   random_state=42,
                                )
        
        self.interactions_full_indexed_df = self.interactions_df.set_index('userId')
        self.interactions_train_indexed_df = interactions_train_df.set_index('userId')
        self.interactions_test_indexed_df = interactions_test_df.set_index('userId')
        

        return interactions_train_df,interactions_test_df
    
        
                
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
               