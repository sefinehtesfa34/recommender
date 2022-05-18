import sklearn
import pandas as pd
import numpy as np
import random
import scipy
import nltk
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
from scipy.sparse.linalg import svds
from scipy.sparse import csr_matrix
from nltk.corpus import stopwords
import math 
import random

from articleRecommender.recommender import PopularityRecommender
class PreprocessingModel:
    def __init__(self,interactions_json,article_json,eventStrength):
        self.interaction_json=interactions_json
        self.article_json=article_json
        self.eventStrength=eventStrength
        self.interactions_df=pd.DataFrame(self.interaction_json)
        self.article_df=pd.DataFrame(self.article_json)
        self.preporcessor()
        self.popularity_model=PopularityRecommender(self.interactions_df,self.article_df)
        self.recommended=None
        
        
        self.printer()
        # self.trainTestSpliter()
    def getUserId(self,userId):
        self.recommended=self.popularity_model.recommend_items(userId)
    def printer(self):
        print(self.interactions_df )
        
    def preporcessor(self):
        self.interactions_df['eventStrength'] = self.interactions_df['eventType'].apply(lambda x: self.eventStrength[x])
        def smooth_user_preference(x):
            return math.log(1+x, 2)
    
        self.interactions_df = self.interactions_df \
                    .groupby(['userId', 'contentId'])['eventStrength'].sum().apply(smooth_user_preference).reset_index()
    def trainTestSpliter(self):
        interactions_train_df, interactions_test_df = train_test_split(self.interactions_df,
                                 
                                   test_size=0.20,
                                   random_state=42,
                                   #    stratify=self.interactions_df['userId']
                                )
        
        self.interactions_full_indexed_df = self.interactions_df.set_index('userId')
        self.interactions_train_indexed_df = interactions_train_df.set_index('userId')
        self.interactions_test_indexed_df = interactions_test_df.set_index('userId')
        

        return interactions_train_df,interactions_test_df
    
        
                
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
               