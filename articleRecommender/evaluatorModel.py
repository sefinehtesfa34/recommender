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

class ModelEvaluator:
    def __init__(self,train,test,full,artices_df) -> None:
        self.train_set=train
        self.test_set=test 
        self.full_set=full 
        self.articles_df=artices_df
        
        
        EVAL_RANDOM_SAMPLE_NON_INTERACTED_ITEMS = 100 
    def get_items_interacted(self,person_id, interactions_df):
    # Get the user's data and merge in the movie information.
        interacted_items = interactions_df.loc[person_id]['contentId']
        return set(interacted_items if type(interacted_items) == pd.Series else [interacted_items])
# Top-N accuracy metrics consts
    def get_not_interacted_items_sample(self, person_id, sample_size, seed=42):
        interacted_items = self.get_items_interacted(person_id, self.full_set)
        all_items = set(self.articles_df['contentId'])
        non_interacted_items = all_items - interacted_items

        random.seed(seed)
        non_interacted_items_sample = random.sample(non_interacted_items, sample_size)
        return set(non_interacted_items_sample)


     
        
    