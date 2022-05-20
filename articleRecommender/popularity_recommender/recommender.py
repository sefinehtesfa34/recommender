# #Computes the most popular items

class PopularityRecommender:
    
    MODEL_NAME = 'Popularity'
    
    def __init__(self, popularity_df, items_df=None):
        self.popularity_df = popularity_df
        self.compute_popular_items()
        self.items_df = items_df
        
    def compute_popular_items(self):
        self.popularity_df=self.popularity_df.groupby('contentId')['eventStrength']\
                                    .sum()\
                                    .sort_values(ascending=False)\
                                    .reset_index()
        
    def get_model_name(self):
        return self.MODEL_NAME
        
    def recommend_items(self, user_id, items_to_ignore=[], topn=10, verbose=False):
        # Recommend the more popular items that the user hasn't seen yet.
        recommendations_df = self.popularity_df[~self.popularity_df['contentId'].isin(items_to_ignore)] \
                               .sort_values('eventStrength', ascending = False) \
                               .head(topn)['contentId']

        if verbose:
            if self.items_df is None:
                raise Exception('"items_df" is required in verbose mode')

            recommendations_df = recommendations_df.merge(\
                                    self.items_df, \
                                    how = 'left', 
                                    left_on = 'contentId', 
                                    right_on = 'contentId')[['eventStrength', 'contentId', 'title', 'url', 'lang']]


        return recommendations_df
    