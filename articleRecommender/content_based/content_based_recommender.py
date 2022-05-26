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
        self.vectorizerModel=TfidfVectorizerModel(articles_df)
        self.build_users_profiles()        
        self.contentBasedRecommender=ContentBasedRecommender(self.user_profiles,articles_df,articles_df["contentId"].tolist())
    def recommend_with_userId(self,userId):
        
        return self.contentBasedRecommender.recommend_items(userId)
           
    def get_item_profile(self,item_id):
        # idx = self.vectorizerModel.item_ids.index(item_id)
        item_profile =self.vectorizerModel.tfidf_matrix[item_id:item_id+1]
        # print(np.asarray(item_profile))
        return np.asarray(item_profile)


    def get_item_profiles(self,ids):
        item_profiles_list = [self.get_item_profile(x) for x in ids]
        print("The problem is inside the get_item_profiles function in ")
        for item in item_profiles_list:
            print(item.shape)
        item_profiles = scipy.sparse.vstack(item_profiles_list).toarry()
        #Here above is the problem
        
        return item_profiles

    def build_users_profile(self,userId, interactions_indexed_df):
        interactions_person_df = interactions_indexed_df.loc[userId]
        
        user_item_profiles = self.get_item_profiles(interactions_person_df['contentId'])
        user_item_strengths = np.array(interactions_person_df['eventStrength']).reshape(-1,1)
        #Weighted average of item profiles by the interactions strength
        # print(user_item_profiles)
        # print(user_item_strengths)
        user_item_strengths_weighted_avg = np.sum(user_item_profiles.multiply(user_item_strengths), axis=0) / np.sum(user_item_strengths)
        user_profile_norm = sklearn.preprocessing.normalize(user_item_strengths_weighted_avg)
        print()
        print("The norms of the matrix")
        print()
        print(user_profile_norm[0])
        
        return user_profile_norm

    def build_users_profiles(self): 
        
        interactions_indexed_df = self.interactions_train_df.set_index('userId')
        self.user_profiles = {}
        for userId in interactions_indexed_df.index.unique():
            self.user_profiles[userId] = self.build_users_profile(userId, interactions_indexed_df)
        