import matplotlib.pyplot as plt 
import seaborn as sns
from sklearn.cluster import KMeans
import gensim 
from gensim.models.doc2vec import Doc2Vec,TaggedDocument
import sklearn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import random
import scipy
import nltk
import time
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


# nltk.download('stopwords')
#Ignoring stopwords (words with no semantics) from English and Portuguese (as we have a corpus with mixed languages)
stopwords_list = stopwords.words('english') + stopwords.words('portuguese')

#Trains a model whose vectors size is 5000, composed by the main unigrams and bigrams found in the corpus, ignoring stopwords
vectorizer = CountVectorizer(analyzer='word',
                     ngram_range=(1, 2),
                     min_df=0.003,
                     max_df=0.5,
                     max_features=5000,
                     stop_words=stopwords_list)

# item_ids = articles_df['contentId'].tolist()
# tfidf_matrix = vectorizer.fit_transform(articles_df['title'] + "" + articles_df['text'])
# tfidf_feature_names = vectorizer.get_feature_names()
# tfidf_matrix