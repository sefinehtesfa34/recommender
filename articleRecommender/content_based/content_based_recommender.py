import sklearn
import numpy as np
import scipy
from sklearn.model_selection import train_test_split
from articleRecommender.content_based.content_based_model.contentBasedRecommnder import ContentBasedRecommender
from articleRecommender.content_based.word_vetorizer.tfidf_vectorizer import TfidfVectorizerModel
from sklearn.model_selection import train_test_split
class ContentBasedRecommenderModel:
    def __init__(self,articles_df,interactions_df):
        
        self.interactions_train_df,self.interactions_test_df = train_test_split(interactions_df,\
                                                                                    test_size=0.20,\
                                                                                random_state=42)
        self.articles_df=articles_df
        self.item_ids=self.articles_df["contentId"].tolist()
        self.vectorizerModel=TfidfVectorizerModel(articles_df)
        self.user_profiles=self.build_users_profiles()        
        self.contentBasedRecommender=ContentBasedRecommender(self.user_profiles,\
                                                            articles_df,\
                                                            self.item_ids)
        
    def items_recommender(self,userId):
        return self.contentBasedRecommender.recommend_items(userId)
    def get_item_profile(self,item_id):
        idx = self.item_ids.index(item_id)
        item_profile = self.vectorizerModel.tfidf_matrix[idx:idx+1]
        return item_profile

    def get_item_profiles(self,ids):
        item_profiles_list = [self.get_item_profile(x) for x in ids]
        item_profiles = scipy.sparse.vstack(item_profiles_list)
        return item_profiles

    def build_users_profile(self,person_id, interactions_indexed_df):
        interactions_person_df = interactions_indexed_df.loc[person_id]
        user_item_profiles = self.get_item_profiles(interactions_person_df['contentId'])
        
        user_item_strengths = np.array(interactions_person_df['eventStrength']).reshape(-1,1)
        user_item_strengths_weighted_avg = np.sum(user_item_profiles.multiply(user_item_strengths), axis=0) / np.sum(user_item_strengths)
        user_profile_norm = sklearn.preprocessing.normalize(user_item_strengths_weighted_avg)
        return user_profile_norm

    def build_users_profiles(self): 
        interactions_indexed_df = self.interactions_train_df[self.interactions_train_df['contentId'] \
                                                    .isin(self.articles_df['contentId'])].set_index('userId')
        user_profiles = {}
        for person_id in interactions_indexed_df.index.unique():
            user_profiles[person_id] = self.build_users_profile(person_id, interactions_indexed_df)
        return user_profiles
    