import os
import re
import time
import pandas as pd
import numpy as np
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pattern
from pattern.en import lemma, lexeme
from num2words import num2words
import nltk
nltk.download('popular')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from autocorrect import Speller
from rank_bm25 import BM25Okapi

__all__ = ['preprocess', 'create_tfidf_features', 'calculate_similarity', 'show_similar_documents', 'create_index',
           'index_data', 'index_batch', 'run_query_loop', 'handle_query']

# Create your connection.
cnx = sqlite3.connect('data.sqlite')

#Read the Data
df = pd.read_sql_query("SELECT * FROM example", cnx)
titles=[title for title in df['title']]
html_codes=[html for html in df['html']]
urls = [url for url in df['url']]
keywords = [keywords for keywords in df['keywords']]

#Set preprocessors
wordnet_lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
spell = Speller()

#BM-25
corpus = [(body+' '+title).lower() for title, body in zip(df['title'], df['keywords'])]
tokenized_corpus = [doc.split(" ") for doc in corpus]

bm25 = BM25Okapi(tokenized_corpus)

def preprocess(text=None,partial=False):
    if text is None:
        return ''
    else:
        #to lower case
        text = text.lower()

        #Remove Special characters
        text = ''.join(e for e in text if e.isalnum() or e==' ')

        #Tokenize the cleansed String
        tokenization = word_tokenize(text)

        #Remove stopwords
        filtered = [w for w in tokenization if not w in stop_words]

        preprocessed = []
        # convert numeral to its word equivalent
        for word in filtered:
            if(word.isnumeric()):
                modified = num2words(word)
                for char in modified:
                    if(char.isalpha()):
                        pass
                    else:
                        if(char==' '):
                            pass
                        else:
                            char=' '
                preprocessed = preprocessed + modified.split(' ')
            else:
                try:
                    word,tag = pos_tag(word_tokenize(word))[0]
                    wntag = tag[0].lower()
                    wntag = wntag if wntag in ['a', 'r', 'n', 'v'] else None
                    word = wordnet_lemmatizer.lemmatize(word,wntag) if wntag else word
                except LookupError:
                    word = word
                preprocessed.append(word)

        #Return the cleansed String
        text = ' '.join(preprocessed)
        if partial:
            print('Partially preprocessed : '+text)
            return text
        #correct spelling
        text = spell(text)
        return text


def create_tfidf_features(corpus, max_features=5000, max_df=0.95, min_df=2):
    """ Creates a tf-idf matrix for the `corpus` using sklearn. """
    tfidf_vectorizor = TfidfVectorizer(decode_error='replace', strip_accents='unicode', analyzer='word',
                                       stop_words='english', ngram_range=(1, 1), max_features=max_features,
                                       norm='l2', use_idf=True, smooth_idf=True, sublinear_tf=True,
                                       max_df=max_df, min_df=min_df)
    X = tfidf_vectorizor.fit_transform(corpus)
    print('tfidf matrix successfully created.')
    return X, tfidf_vectorizor

def calculate_similarity(X, vectorizor, query, top_k=5):
    """ Vectorizes the `query` via `vectorizor` and calculates the cosine similarity of
    the `query` and `X` (all the documents) and returns the `top_k` similar documents."""

    # Vectorize the query to the same length as documents
    query_vec = vectorizor.transform(query)
    # Compute the cosine similarity between query_vec and all the documents
    cosine_similarities = cosine_similarity(X,query_vec).flatten()
    # Sort the similar documents from the most similar to less similar and return the indices
    most_similar_doc_indices = np.argsort(cosine_similarities, axis=0)[:-top_k-1:-1]
    return (most_similar_doc_indices, cosine_similarities)

def show_similar_documents(df, cosine_similarities, similar_doc_indices):
    """ Prints the most similar documents using indices in the `similar_doc_indices` vector."""
    counter = 1
    objects = {}
    print('TF-IDF Top 5 Results'+'\n')
    for index in similar_doc_indices:
        object = {}
        object['score'] = cosine_similarities[index]
        object['document_number'] = df[index].split(' ')[0]
        object['keywords'] = df[index]
        object['title'] = titles[int(object['document_number'])]
        print('Top-{}, Similarity = {}'.format(counter, cosine_similarities[index]))
        print('body: {}, '.format(df[index]))
        print('\n')
        objects[str(counter)]=object
        counter += 1
    return objects

def run_bm25(query,part=False):
    """ Use BM-25 Algorithm to return top 5 results"""
    query=preprocess(query,part)
    tokenized_query = query.split(" ")
    doc_scores = bm25.get_scores(tokenized_query)
    results = bm25.get_top_n(tokenized_query, corpus)
    # for result in results:
    #     print(result+'\n\n')
    # print(sorted(doc_scores)[::-1][:5])
    scores = sorted(doc_scores)[::-1][:5]
    object = {}
    print('BM-25 Top 5 Results'+'\n')
    for i in range(1,6):
        doc_num=results[i-1].split(' ')[0]
        # object[str(i)] = {'score':str(scores[i-1]/100),'document_number':doc_num,'keywords':keywords[int(doc_num)],'title':titles[int(doc_num)]}
        object[str(i)] = {'score':str(scores[i-1]),'document_number':doc_num,'keywords':keywords[int(doc_num)],'title':titles[int(doc_num)]}
        print('Top-{}, Similarity = {}'.format(str(i), str(scores[i-1])))
        print('body: {} '.format(keywords[int(doc_num)]))
        print('\n')
    return object
