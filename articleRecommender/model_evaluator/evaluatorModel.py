import pandas as pd
import random
import random

class ModelEvaluator:
    def __init__(self,train,test,full,artices_df) -> None:
        self.train_set_df=train
        self.test_set_df=test 
        self.full_set_df=full 
        self.articles_df=artices_df
        self.EVAL_RANDOM_SAMPLE_NON_INTERACTED_ITEMS = 100 
    def get_items_interacted(self,person_id, interactions_df):
        interacted_items = interactions_df.loc[person_id]['contentId']
        return set(interacted_items if type(interacted_items) == pd.Series else [interacted_items])
    def get_not_interacted_items_sample(self, person_id, sample_size, seed=42):
        interacted_items = self.get_items_interacted(person_id, self.full_set_df)
        all_items = set(self.articles_df['contentId'])
        non_interacted_items = all_items - interacted_items

        random.seed(seed)
        non_interacted_items_sample = random.sample(non_interacted_items, sample_size)
        return set(non_interacted_items_sample)
    def _verify_hit_top_n(self, item_id, recommended_items, topn):        
            try:
                index = next(i for i, c in enumerate(recommended_items) if c == item_id)
            except:
                index = -1
            hit = int(index in range(0, topn))
            return hit, index
    def evaluate_model_for_user(self, model, person_id):
        interacted_values_testset = self.test_set_df.loc[person_id]
        if type(interacted_values_testset['contentId']) == pd.Series:
            person_interacted_items_testset = set(interacted_values_testset['contentId'])
        else:
            person_interacted_items_testset = set([int(interacted_values_testset['contentId'])])  
        interacted_items_count_testset = len(person_interacted_items_testset) 

        person_recs_df = model.recommend_items(person_id, 
                                               items_to_ignore=self.get_items_interacted(person_id, 
                                                                                    self.train_set_df), 
                                               topn=10000000000)

        hits_at_5_count = 0
        hits_at_10_count = 0
        for item_id in person_interacted_items_testset:
            non_interacted_items_sample = self.get_not_interacted_items_sample(person_id, 
                                                                          sample_size=self.EVAL_RANDOM_SAMPLE_NON_INTERACTED_ITEMS, 
                                                                          seed=item_id%(2**32))

            items_to_filter_recs = non_interacted_items_sample.union(set([item_id]))

            valid_recs_df = person_recs_df[person_recs_df['contentId'].isin(items_to_filter_recs)]                    
            valid_recs = valid_recs_df['contentId'].values
            hit_at_5, index_at_5 = self._verify_hit_top_n(item_id, valid_recs, 5)
            hits_at_5_count += hit_at_5
            hit_at_10, index_at_10 = self._verify_hit_top_n(item_id, valid_recs, 10)
            hits_at_10_count += hit_at_10

        recall_at_5 = hits_at_5_count / float(interacted_items_count_testset)
        recall_at_10 = hits_at_10_count / float(interacted_items_count_testset)

        person_metrics = {'hits@5_count':hits_at_5_count, 
                          'hits@10_count':hits_at_10_count, 
                          'interacted_count': interacted_items_count_testset,
                          'recall@5': recall_at_5,
                          'recall@10': recall_at_10}
        return person_metrics
    def evaluate_model(self, model):
        people_metrics = []
        for idx, person_id in enumerate(list(self.test_set_df.index.unique().values)):
            person_metrics = self.evaluate_model_for_user(model, person_id)  
            person_metrics['_person_id'] = person_id
            people_metrics.append(person_metrics)
        detailed_results_df = pd.DataFrame(people_metrics) \
                            .sort_values('interacted_count', ascending=False)
        
        global_recall_at_5 = detailed_results_df['hits@5_count'].sum() / float(detailed_results_df['interacted_count'].sum())
        global_recall_at_10 = detailed_results_df['hits@10_count'].sum() / float(detailed_results_df['interacted_count'].sum())
        
        global_metrics = {'modelName': model.get_model_name(),
                          'recall@5': global_recall_at_5,
                          'recall@10': global_recall_at_10}    
        return global_metrics, detailed_results_df
    



 
        
    