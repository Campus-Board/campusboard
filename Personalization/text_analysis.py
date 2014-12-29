# -*- coding: utf-8 -*-
__author__ = 'mac'
from os.path import join
import csv

DATA_PATH = "./Data"
PERSONALIZATION_PATH = "./Personalization/"

NEWS_IC = "noticias-ic-06-today.csv"
NEWS = "noticias-unicamp.csv"
PALES = "palestras.csv"
CDC = "expos-cdc.csv"
LAGO = "casa-do-lago.csv"
ANNOT = "annotations.csv"
LABEL = "labels.csv"
TAXONOMY = 'taxonomy.txt'
TAXONOMY_LEN = 16
BOW_CORPUS = PERSONALIZATION_PATH + "bcorpus"
DICT = PERSONALIZATION_PATH + "dict"
MODEL = PERSONALIZATION_PATH + "model"
CLASSIFIER = PERSONALIZATION_PATH + "classifier"
TOPICS = 20

#def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
#    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
#    for row in csv_reader:
#        yield [cell.encode('utf-8') for cell in row]

def load_news():
    reader = csv.reader(file(join(DATA_PATH, NEWS)), delimiter='$', quotechar='#')
    res = []
    for row in reader:
        [date, title, content] = row
        res.append(title + "\n" + content)
    return res

def load_news_ic():
    reader = csv.reader(file(join(DATA_PATH, NEWS_IC)), delimiter='$', quotechar='#')
    res = []
    for row in reader:
        [title, content] = row
        res.append(title + "\n" + content)
    return res

def load_expo_cdc():
    print DATA_PATH + " --- " + CDC
    print join(DATA_PATH, CDC)
    reader = csv.reader(file(join(DATA_PATH, CDC)), delimiter='$', quotechar='#')
    res = []
    for row in reader:
        [inid, endd, inih, endh, title, content] = row
        res.append(str(title + "\n" + content))
    return res

def load_palestras():
    reader = csv.reader(file(join(DATA_PATH, PALES)), delimiter='$', quotechar='#')
    res = []
    for row in reader:
        [date, title, content] = row
        res.append(title + "\n" + content)
    return res

def load_lago():
    reader = csv.reader(file(join(DATA_PATH, LAGO)), delimiter='$', quotechar='#')
    res = []
    for row in reader:
        [ini, end, title, content] = row
        res.append(title + "\n" + content)
    return res

def load_labels():
    reader = csv.reader(file(join(DATA_PATH, LABEL)), delimiter=',')
    res = []
    for row in reader:
        for cell in row:
            res.append(int(cell))
    return res

# Returns an array with the content
def all_content():
    corpus = []
    corpus += load_expo_cdc()
    corpus += load_lago()
    corpus += load_news()
    corpus += load_news_ic()
    corpus += load_palestras()
    return corpus

import numpy as np

def load_annotations():
    #print "load annotations"
    reader = csv.reader(file(join(DATA_PATH, ANNOT)), delimiter=',', quotechar='"')
    res = []
    for row in reader:
        res2 = []
        for cell in row:
            res2.append(cell)
        res.append(res2)
    res = np.array(res)
    res = res[1:,:]
    #print res
    for i in range(len(res)):
        for j in range(len(res[0])):
            res[i][j] = int(res[i][j])
    return res


def generate_word_cloud(corpora, outfile):
    raise Exception("Implement this!")

from nltk import word_tokenize
from nltk.stem import RSLPStemmer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import string

def preprocessing(corpora):
    stemmer = RSLPStemmer()
    stemmer2 = PorterStemmer()
    stp = stopwords.words('portuguese')
    #stp.append('')
    stp.append('ainda')
    res = []
    for i in range(len(corpora)):
        corpora[i] = str(corpora[i]).lower()
        corpora[i] = corpora[i].translate(None, string.punctuation)
        corpora[i] = corpora[i].decode('utf-8')
        corpora[i] = corpora[i].replace(u'”',u'')
        corpora[i] = corpora[i].replace(u'“',u'')
        corpora[i] = corpora[i].replace(u'–',u'')
        res2 = []
        for t in word_tokenize(corpora[i]):
            if t in stp:
                continue
            if(any(char.isdigit() for char in t)==False):
                res2.append(stemmer2.stem(stemmer.stem(t)))
        res.append(res2)
    return res

def preprocessing_wordcloud(corpora):
    stp = stopwords.words('portuguese')
    stp += stopwords.words('english')
    stp += ['ainda', 'el', 'la', 'en', 'con', 'sob' ]
    res = ""
    for i in range(len(corpora)):
        corpora[i] = corpora[i].lower()
        corpora[i] = corpora[i].translate(None, string.punctuation)
        corpora[i] = corpora[i].decode('utf-8')
        corpora[i] = corpora[i].replace(u'”',u'')
        corpora[i] = corpora[i].replace(u'“',u'')
        corpora[i] = corpora[i].replace(u'–',u'')
        for t in word_tokenize(corpora[i]):
            if t in stp:
                continue
            if(any(char.isdigit() for char in t)==False):
                #print t.decode('utf-8')
                res += " " + t
    return res

def save_wordclouds():
    text = preprocessing_wordcloud(load_expo_cdc())
    of = open(join(DATA_PATH, CDC + "_cloud.txt"), "wb+")
    of.write(text.encode('utf-8'))
    of.close()
    text = preprocessing_wordcloud(load_lago())
    of = open(join(DATA_PATH, LAGO + "_cloud.txt"), "wb+")
    of.write(text.encode('utf-8'))
    of.close()
    text = preprocessing_wordcloud(load_news())
    of = open(join(DATA_PATH, NEWS + "_cloud.txt"), "wb+")
    of.write(text.encode('utf-8'))
    of.close()
    text = preprocessing_wordcloud(load_news_ic())
    of = open(join(DATA_PATH, NEWS_IC + "_cloud.txt"), "wb+")
    of.write(text.encode('utf-8'))
    of.close()
    text = preprocessing_wordcloud(load_palestras())
    of = open(join(DATA_PATH, PALES + "_cloud.txt"), "wb+")
    of.write(text.encode('utf-8'))
    of.close()

from gensim import corpora, models, similarities
from gensim.models.ldamodel import LdaModel
import gensim

#save_wordclouds()

from sklearn.externals import joblib

def generate_model():
    np.set_printoptions(precision=2)
    corpus = []
    corpus += load_expo_cdc()
    corpus += load_lago()
    corpus += load_news()
    corpus += load_news_ic()
    corpus += load_palestras()
    corpus = preprocessing(corpus)
    dictionary = corpora.Dictionary(corpus)
    bow_corpus = [dictionary.doc2bow(text) for text in corpus]

    dictionary.save(DICT)
    corpora.MmCorpus.serialize(BOW_CORPUS, bow_corpus)

    bow2 = np.concatenate((bow_corpus, bow_corpus), axis=0)
    bow2 = np.concatenate((bow2, bow2), axis=0)
    bow2 = np.concatenate((bow2, bow2), axis=0)
    TOPICS = 20
    model = LdaModel(bow2, id2word=dictionary, num_topics=TOPICS, iterations=100, passes=15)
    model.save(MODEL)

    lda_corpus = [model[vector] for vector in bow2]
    lda_dense = gensim.matutils.corpus2dense(lda_corpus, num_terms=TOPICS).transpose()
    """
    tfidf = models.TfidfModel(bow_corpus)
    tfidf_corpus = [tfidf[vector] for vector in bow_corpus]
    tfidf_dense = gensim.matutils.corpus2dense(tfidf_corpus, num_terms=len(dictionary)).transpose()
    """
    classifier = LogisticRegression()
    labels = load_labels()
    labels2 = labels
    labels2 += labels2
    labels2 += labels2
    labels2 += labels2
    classifier.fit(lda_dense, labels2)
    joblib.dump(classifier, CLASSIFIER, compress=9)
    #print "LDA results"
    probs = classifier.predict_proba(lda_dense)
    #rint probs

class TextAnalyzer(object):
    def read_model(self):
        self.dictionary = corpora.Dictionary.load(DICT)
        self.bow_corpus = corpora.MmCorpus(BOW_CORPUS)
        self.lda_model = LdaModel.load(MODEL)
        self.logit_classifier = joblib.load(CLASSIFIER)

        corpus = []
        corpus += load_expo_cdc()
        corpus += load_lago()
        corpus += load_news()
        corpus += load_news_ic()
        corpus += load_palestras()
        corpus = preprocessing(corpus)

        test_bow = [self.dictionary.doc2bow(text) for text in corpus]
        lda_corpus = [self.lda_model[bow] for bow in test_bow]
        lda_dense = gensim.matutils.corpus2dense(lda_corpus, num_terms=TOPICS).transpose()
        probs = self.logit_classifier.predict_proba(lda_dense)
        #print "RESULTS IN READED MODEL"
        #print probs
    def predict(self, text):
        text = [text]
        text = preprocessing(text)
        #print text
        test_bow = [self.dictionary.doc2bow(row) for row in text]
        lda_corpus = [self.lda_model[bow] for bow in test_bow]
        lda_dense = gensim.matutils.corpus2dense(lda_corpus, num_terms=TOPICS).transpose()
        probs = self.logit_classifier.predict_proba(lda_dense)
        return probs[0]

import sklearn

def similarity(x, y, metric=None):
    dist = sklearn.metrics.pairwise.pairwise_distances([x],[y])
    #print len(dist)
    #print len(dist[0])
    return dist[0]

################## FAST PERSONALIZATION API ####################

def default_profile():
    return [0.5]*TAXONOMY_LEN

def cs_profile():
    profile =  [0.0]*TAXONOMY_LEN
    for i in range(12,TAXONOMY_LEN):
        profile[i] = 1
    return profile

def cs_and_artist_profile():
    profile = [0.0]*TAXONOMY_LEN
    for i in range(0, 5):
        profile[i] = 1
    for i in range(12,TAXONOMY_LEN):
        profile[i] = 1
    return profile

def update_profile_by_data(profile, analyzer, data, delta = 0.1):
    labels = analyzer.predict(data)
    max_ = max(labels)
    min_ = min(labels)
    for i in range(len(labels)):
        labels[i] = (labels[i]-min_)/(max_-min_)
    assert len(labels) == len(profile)
    for i in range(len(profile)):
        profile[i] = profile[i] * 0.9 + labels[i] * 0.1
    return profile

def update_profile_by_data(profile, data, delta = 0.3):
    analyzer = TextAnalyzer()
    analyzer.read_model()
    assert len(profile) == TAXONOMY_LEN
    labels = analyzer.predict(data)
    max_ = max(labels)
    min_ = min(labels)
    for i in range(len(labels)):
        labels[i] = (labels[i]-min_)/(max_-min_)
    assert len(labels) == len(profile)
    for i in range(len(profile)):
        profile[i] = profile[i] * (1-delta) + labels[i] * delta
    return profile

def get_personalized_content(model, profile_array, how_much_documents):
    assert len(profile_array) == TAXONOMY_LEN
    documents = all_content()
    # RANK RESULTS
    sims = []
    for i in range(len(documents)):
        doc = documents[i]
        doc_profile = model.predict(doc)
        sims.append((similarity(profile_array, doc_profile), i))
    sims.sort()
    result = []
    for i in range(min(len(sims), how_much_documents)):
        (val, idx) = sims[i]
        result.append(documents[idx])
    return result

def get_personalized_content(profile_array, k, documents):
    model = TextAnalyzer()
    model.read_model()
    assert len(profile_array) == TAXONOMY_LEN
    sims = []
    for i in range(len(documents)):
        doc = documents[i]

        doc_profile = model.predict(doc.message.encode('utf8'))
        sims.append((similarity(profile_array, doc_profile), i))
    sims.sort()
    result = []
    for i in range(min(len(sims), k)):
        (val, idx) = sims[i]
        result.append(documents[idx])
    k = min(k, len(result))
    return result[:k]

# EXAMPLE OF USE
# TWO considerations:
# - DATA_PATH ( check the top of this file ) should be point to *.csv file that contain the documents
# - The models files ( Personalization/* ) should be in the file where the main application is running

def example():
    model = TextAnalyzer()
    # this call load the model from the directory where Personalization/text_analysis.py is saved
    model.read_model()

    default = default_profile()
    cs = cs_profile()
    cs_artist = cs_and_artist_profile()

    res = get_personalized_content(model, default, 4)
    print "Content for default"
    for item in res:
        print item
        print "\n#############################\n"
    res = get_personalized_content(model, cs, 4)
    print "Content for cs man"
    for item in res:
        print item
        print "\n#############################\n"
    print len(cs)
    print len(cs_artist)
    res = get_personalized_content(model, cs_artist, 4)
    print "Content for cs and artist man"
    for item in res:
        print item
        print "\n#############################\n"

#example()

# UPDATE PROFILE TEST
def testAll():
    analyzer = TextAnalyzer()
    analyzer.read_model()
    corpus = []
    corpus += load_expo_cdc()
    corpus += load_lago()
    corpus += load_news()
    corpus += load_news_ic()
    corpus += load_palestras()

    profile = default_profile();
    print profile
    profile = update_profile_by_data(profile, analyzer, corpus[0])
    print profile


