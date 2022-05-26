import pandas
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

class TfidfVectorizerModel:
    def __init__(self,articles_df) -> None:
        self.articles_df=pandas.DataFrame(articles_df)
        print(self.articles_df.columns)
        self.stopWordGenerator()
        self.vectorize()
        self.tfidfMatrixGenerator()
        self.articleCleaner()
        
    def stopWordGenerator(self):
        self.stopwords_list = stopwords.words('english') + stopwords.words('portuguese')
    def vectorize(self):
        self.vectorizer=TfidfVectorizer(analyzer='word',
                     ngram_range=(1, 2),
                     min_df=0.003,
                     max_df=0.5,
                     max_features=5000,
                     stop_words=self.stopwords_list)
    def tfidfMatrixGenerator(self):
        self.item_ids = self.articles_df.set_index('contentId').index.tolist()
        self.tfidf_matrix = self.vectorizer.fit_transform(self.articles_df['title'] + "" + self.articles_df['content'])
        self.tfidf_feature_names = self.vectorizer.get_feature_names_out()
        return self.tfidf_matrix
    def articleCleaner(self):
        
        self.article=(self.articles_df['title'] + "" + self.articles_df['content']).fillna("")
        
        
        