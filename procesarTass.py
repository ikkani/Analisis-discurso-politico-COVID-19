from procesarTuits import *
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import preprocessing
from os import listdir
from os.path import isfile, join
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from spacy.lang.es.stop_words import STOP_WORDS
from lxml import objectify
import langid
import pandas as pd


stop_words = set(stopwords.words('spanish'))

if isfile('./TASS/general-test-tagged-3l.csv'):
	general_test_tagged_3l = pd.read_csv('./TASS/general-test-tagged-3l.csv', encoding='utf-8')
else:
	xml = objectify.parse(open('./TASS/general-test-tagged-3l.xml' , encoding='utf-8'))
	general_test_tagged_3l = pd.DataFrame(columns=('content','polarity'))
	tweets = xml.getroot().getchildren()
	for tweet in tweets:
		if str(tweet.sentiments.polarity.value).lower() == 'none':
			continue
		fila = dict(zip(['content','polarity'], [tweet.content, tweet.sentiments.polarity.value]))
		general_test_tagged_3l = general_test_tagged_3l.append(fila, ignore_index = True)
	general_test_tagged_3l.to_csv('./TASS/general-test-tagged-3l.csv', index = False, encoding = 'utf-8')


if isfile('./TASS/general-train-tagged-3l.csv'):
	general_train_tagged_3l = pd.read_csv('./TASS/general-train-tagged-3l.csv', encoding='utf-8')
else:
	xml = objectify.parse(open('./TASS/general-train-tagged-3l.xml' , encoding='utf-8'))
	general_train_tagged_3l = pd.DataFrame(columns=('content','polarity'))
	tweets = xml.getroot().getchildren()
	for tweet in tweets:
		if str(tweet.sentiments.polarity.value).lower() == 'none':
			continue
		fila = dict(zip(['content','polarity'], [tweet.content, tweet.sentiments.polarity.value]))
		general_train_tagged_3l = general_train_tagged_3l.append(fila, ignore_index = True)
	general_train_tagged_3l.to_csv('./TASS/general-train-tagged-3l.csv', index = False, encoding = 'utf-8')


if isfile('./TASS/intertass-ES-development-tagged.csv'):
	intertass_ES_development_tagged = pd.read_csv('./TASS/intertass-ES-development-tagged.csv', encoding='utf-8')
else:
	xml = objectify.parse(open('./TASS/intertass-ES-development-tagged.xml' , encoding='utf-8'))
	intertass_ES_development_tagged = pd.DataFrame(columns=('content','polarity'))
	tweets = xml.getroot().getchildren()
	for tweet in tweets:
		if str(tweet.sentiment.polarity.value).lower() == 'none':
			continue
		fila = dict(zip(['content','polarity'], [tweet.content, tweet.sentiment.polarity.value]))
		intertass_ES_development_tagged = intertass_ES_development_tagged.append(fila, ignore_index = True)
	intertass_ES_development_tagged.to_csv('./TASS/intertass-ES-development-tagged.csv', index = False, encoding = 'utf-8')


if isfile('./TASS/intertass-ES-train-tagged.csv'):
	intertass_ES_train_tagged = pd.read_csv('./TASS/intertass-ES-train-tagged.csv', encoding='utf-8')
else:
	xml = objectify.parse(open('./TASS/intertass-ES-train-tagged.xml' , encoding='utf-8'))
	intertass_ES_train_tagged = pd.DataFrame(columns=('content','polarity'))
	tweets = xml.getroot().getchildren()
	for tweet in tweets:
		if str(tweet.sentiment.polarity.value).lower() == 'none':
			continue
		fila = dict(zip(['content','polarity'], [tweet.content, tweet.sentiment.polarity.value]))
		intertass_ES_train_tagged = intertass_ES_train_tagged.append(fila, ignore_index = True)
	intertass_ES_train_tagged.to_csv('./TASS/intertass-ES-train-tagged.csv', index = False, encoding = 'utf-8')


if isfile('./TASS/politics-test-tagged.csv'):
	politics_test_tagged = pd.read_csv('./TASS/politics-test-tagged.csv', encoding='utf-8')
else:
	xml = objectify.parse(open('./TASS/politics-test-tagged.xml' , encoding='utf-8'))
	politics_test_tagged = pd.DataFrame(columns=('content','polarity'))
	tweets = xml.getroot().getchildren()
	for tweet in tweets:
		if str(tweet.sentiments.polarity.value).lower() == 'none':
			continue
		fila = dict(zip(['content','polarity'], [tweet.content, tweet.sentiments.polarity.value]))
		politics_test_tagged = politics_test_tagged.append(fila, ignore_index = True)
	politics_test_tagged.to_csv('./TASS/politics-test-tagged.csv', index = False, encoding = 'utf-8')


if isfile('./TASS/stompol-test-tagged.csv'):
	stompol_test_tagged = pd.read_csv('./TASS/stompol-test-tagged.csv', encoding='utf-8')
else:
	xml = objectify.parse(open('./TASS/stompol-test-tagged.xml' , encoding='utf-8'))
	stompol_test_tagged = pd.DataFrame(columns=('content','polarity'))
	tweets = xml.getroot().getchildren()
	for tweet in tweets:
		if str(tweet.sentiment.get('polarity')).lower() == 'none':
			continue
		texto = ''
		for t in tweet.itertext():
 			texto += t
		fila = dict(zip(['content','polarity'], [texto, tweet.sentiment.get('polarity')]))
		stompol_test_tagged = stompol_test_tagged.append(fila, ignore_index = True)
	stompol_test_tagged.to_csv('./TASS/stompol-test-tagged.csv', index = False, encoding = 'utf-8')


if isfile('./TASS/stompol-train-tagged.csv'):
	stompol_train_tagged = pd.read_csv('./TASS/stompol-train-tagged.csv', encoding='utf-8')
else:
	xml = objectify.parse(open('./TASS/stompol-train-tagged.xml' , encoding='utf-8'))
	stompol_train_tagged = pd.DataFrame(columns=('content','polarity'))
	tweets = xml.getroot().getchildren()
	for tweet in tweets:
		if str(tweet.sentiment.get('polarity')).lower() == 'none':
			continue
		texto = ''
		for t in tweet.itertext():
 			texto += t
		fila = dict(zip(['content','polarity'], [texto, tweet.sentiment.get('polarity')]))
		stompol_train_tagged = stompol_train_tagged.append(fila, ignore_index = True)
	stompol_train_tagged.to_csv('./TASS/stompol-train-tagged.csv', index = False, encoding = 'utf-8')


if isfile('./TASS/TASS2019_country_ES_dev.csv'):
	TASS2019_country_ES_dev = pd.read_csv('./TASS/TASS2019_country_ES_dev.csv', encoding='utf-8')
else:
	xml = objectify.parse(open('./TASS/TASS2019_country_ES_dev.xml' , encoding='utf-8'))
	TASS2019_country_ES_dev = pd.DataFrame(columns=('content','polarity'))
	tweets = xml.getroot().getchildren()
	for tweet in tweets:
		if str(tweet.sentiment.polarity.value).lower() == 'none':
			continue
		fila = dict(zip(['content','polarity'], [tweet.content, tweet.sentiment.polarity.value]))
		TASS2019_country_ES_dev = TASS2019_country_ES_dev.append(fila, ignore_index = True)
	TASS2019_country_ES_dev.to_csv('./TASS/TASS2019_country_ES_dev.csv', index = False, encoding = 'utf-8')


if isfile('./TASS/TASS2019_country_ES_train.csv'):
	TASS2019_country_ES_train = pd.read_csv('./TASS/TASS2019_country_ES_train.csv', encoding='utf-8')
else:
	xml = objectify.parse(open('./TASS/TASS2019_country_ES_train.xml' , encoding='utf-8'))
	TASS2019_country_ES_train = pd.DataFrame(columns=('content','polarity'))
	tweets = xml.getroot().getchildren()
	for tweet in tweets:
		if str(tweet.sentiment.polarity.value).lower() == 'none':
			continue
		fila = dict(zip(['content','polarity'], [tweet.content, tweet.sentiment.polarity.value]))
		TASS2019_country_ES_train = TASS2019_country_ES_train.append(fila, ignore_index = True)
	TASS2019_country_ES_train.to_csv('./TASS/TASS2019_country_ES_train.csv', index = False, encoding = 'utf-8')


tweets_corpus = pd.concat([
    general_test_tagged_3l,
	general_train_tagged_3l,
	intertass_ES_development_tagged,
	intertass_ES_train_tagged,
	politics_test_tagged,
	stompol_test_tagged,
	stompol_train_tagged,
	TASS2019_country_ES_dev,
	TASS2019_country_ES_train
])

tweets_corpus = tweets_corpus[tweets_corpus.polarity != 'NEU']
tweets_corpus['polarity_bin'] = 0
tweets_corpus.polarity_bin[tweets_corpus.polarity == 'P'] = 1

vectorizer = CountVectorizer(tokenizer = tokenizer)
#LinearSVC() es el clasificador
pipeline = Pipeline([
    ('vect', vectorizer),
    ('cls', LinearSVC(dual = False)),
])
# Aqui definimos el espacio de parámetros a explorar
parameters = {
    'vect__max_df': (0.5, 1.9),
    'vect__min_df': (10, 20,50),
    'vect__max_features': (500, 1000),
    'vect__ngram_range': ((1, 1), (1, 2)),  # unigramas or bigramas
    'cls__C': (0.2, 0.5, 0.7),
    # 'cls__loss': ('squared_hinge','hinge'),
    'cls__max_iter': (500, 1000)
}
grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1 , scoring='roc_auc', verbose = 5)
# grid_search.fit(tweets_corpus.content, tweets_corpus.polarity_bin)

