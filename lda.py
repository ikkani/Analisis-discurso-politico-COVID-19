from cargarCorpus import *
import random
from gensim import corpora
import gensim
from gensim.models import CoherenceModel
import es_core_news_sm
import pandas as pd
import joblib
from procesarTuits import *

meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
"agosto", "septiembre", "octubre", "noviembre", "diciembre"]


nlp = es_core_news_sm.load()
c = joblib.load('./corpusPandas.pkl')

def ldaStemmed(corpus, NUM_TOPICS = 4, fechaMin = '1-1', fechaMax = '1-1',
	random_state=100, update_every=1, chunksize=100, passes=10, alpha='auto', per_word_topics=True,
	iterations = 50, eval_every = 1):
	
	fechaMin = fechaMin.split('-')
	fechaMax = fechaMax.split('-')

	diaMin = int(fechaMin[0])
	diaMax = int(fechaMax[0])
	
	fechaMin = datetime.datetime(2020, int(fechaMin[1]), diaMin)
	fechaMax = datetime.datetime(2020, int(fechaMax[1]), diaMax)
	
	data_words = []

	if fechaMin.month == fechaMax.month:
		corpus = corpus[meses[fechaMin.month-1]].query('dia >= @diaMin and dia <= @diaMax')

	else:
		p1 = corpus[meses[fechaMin.month-1]].query('dia >= @diaMin')
		p2 = pd.DataFrame()
		for i in range(fechaMin.month, fechaMax.month-1):
			p2 = p2.append(corpus[meses[i]])

		p3 = corpus[meses[fechaMax.month-1]].query('dia <= @diaMax')

		corpus = pd.concat([p1,p2,p3])

	corpus = corpus[corpus.lexemas.values == corpus.lexemas.values]

	arrayTokens = corpus.lexemas.values
	for tweet in arrayTokens:
		d = nlp(tweet)
		data_words.append([str(t) for t in d if t.pos_ == 'ADJ' or t.pos_ == 'PROPN' or t.pos_ == 'NOUN'])


	# Build the bigram and trigram models
	bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100) # higher threshold fewer phrases.
	trigram = gensim.models.Phrases(bigram[data_words], threshold=100)  

	# Faster way to get a sentence clubbed as a trigram/bigram
	bigram_mod = gensim.models.phrases.Phraser(bigram)
	trigram_mod = gensim.models.phrases.Phraser(trigram)


	def make_bigrams(texts):
		return [bigram_mod[doc] for doc in texts]

	def make_trigrams(texts):
		return [trigram_mod[bigram_mod[doc]] for doc in texts]

	data_words_bigrams = make_bigrams(data_words)


	id2word = corpora.Dictionary(data_words_bigrams)
	text = data_words_bigrams
	corpus = [id2word.doc2bow(text) for text in data_words_bigrams]

	lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
	                                           id2word=id2word,
	                                           num_topics=NUM_TOPICS, 
	                                           random_state=random_state,
	                                           update_every=update_every,
	                                           chunksize=chunksize,
	                                           passes=passes,
	                                           alpha=alpha,
	                                           per_word_topics=per_word_topics,
	                                           iterations = iterations)

	coherence_model_lda = CoherenceModel(model=lda_model, texts=data_words_bigrams, dictionary=id2word, coherence='c_v')
	coherence_lda = coherence_model_lda.get_coherence()
	# print('\nCoherence Score with ' + str(NUM_TOPICS) + ' topics and ' + str(iterations)  + ' iterations: ' + str(coherence_lda))
	
	return [lda_model, coherence_lda]


def lda(corpus, NUM_TOPICS = 4,
	random_state=100, update_every=1, chunksize=100, passes=10, alpha='auto', per_word_topics=True,
	iterations = 50, eval_every = 1):
	
	
	data_words = []

	arrayTokens = corpus.tokens.values
	for tweet in arrayTokens:
		d = ' '.join(tweet)
		d = nlp(d)
		data_words.append([str(t) for t in d if t.pos_ == 'ADJ' or t.pos_ == 'PROPN' or t.pos_ == 'NOUN'])


	# Build the bigram and trigram models
	bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100) # higher threshold fewer phrases.
	trigram = gensim.models.Phrases(bigram[data_words], threshold=100)  

	# Faster way to get a sentence clubbed as a trigram/bigram
	bigram_mod = gensim.models.phrases.Phraser(bigram)
	trigram_mod = gensim.models.phrases.Phraser(trigram)


	def make_bigrams(texts):
		return [bigram_mod[doc] for doc in texts]

	def make_trigrams(texts):
		return [trigram_mod[bigram_mod[doc]] for doc in texts]

	data_words_bigrams = make_bigrams(data_words)


	id2word = corpora.Dictionary(data_words_bigrams)
	text = data_words_bigrams
	corpus = [id2word.doc2bow(text) for text in data_words_bigrams]

	lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
	                                           id2word=id2word,
	                                           num_topics=NUM_TOPICS, 
	                                           random_state=random_state,
	                                           update_every=update_every,
	                                           chunksize=chunksize,
	                                           passes=passes,
	                                           alpha=alpha,
	                                           per_word_topics=per_word_topics,
	                                           iterations = iterations)

	coherence_model_lda = CoherenceModel(model=lda_model, texts=data_words_bigrams, dictionary=id2word, coherence='c_v')
	coherence_lda = coherence_model_lda.get_coherence()
	# print('\nCoherence Score with ' + str(NUM_TOPICS) + ' topics and ' + str(iterations)  + ' iterations: ' + str(coherence_lda))
	
	return [lda_model, corpus, id2word, coherence_lda]

def ldaFecha(corpus, NUM_TOPICS = 4, fechaMin = '1-1', fechaMax = '1-1',
	random_state=100, update_every=1, chunksize=100, passes=10, alpha='auto', per_word_topics=True,
	iterations = 50, eval_every = 1):
	
	fechaMin = fechaMin.split('-')
	fechaMax = fechaMax.split('-')

	diaMin = int(fechaMin[0])
	diaMax = int(fechaMax[0])
	
	fechaMin = datetime.datetime(2020, int(fechaMin[1]), diaMin)
	fechaMax = datetime.datetime(2020, int(fechaMax[1]), diaMax)
	
	data_words = []

	if fechaMin.month == fechaMax.month:
		corpus = corpus[meses[fechaMin.month-1]].query('dia >= @diaMin and dia <= @diaMax')

	else:
		p1 = corpus[meses[fechaMin.month-1]].query('dia >= @diaMin')
		p2 = pd.DataFrame()
		for i in range(fechaMin.month, fechaMax.month-1):
			p2 = p2.append(corpus[meses[i]])

		p3 = corpus[meses[fechaMax.month-1]].query('dia <= @diaMax')

		corpus = pd.concat([p1,p2,p3])

	arrayTokens = corpus.tokens.values
	for tweet in arrayTokens:
		d = ' '.join(tweet)
		d = nlp(d)
		data_words.append([str(t) for t in d if t.pos_ == 'ADJ' or t.pos_ == 'PROPN' or t.pos_ == 'NOUN'])


	# Build the bigram and trigram models
	bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100) # higher threshold fewer phrases.
	trigram = gensim.models.Phrases(bigram[data_words], threshold=100)  

	# Faster way to get a sentence clubbed as a trigram/bigram
	bigram_mod = gensim.models.phrases.Phraser(bigram)
	trigram_mod = gensim.models.phrases.Phraser(trigram)


	def make_bigrams(texts):
		return [bigram_mod[doc] for doc in texts]

	def make_trigrams(texts):
		return [trigram_mod[bigram_mod[doc]] for doc in texts]

	data_words_bigrams = make_bigrams(data_words)


	id2word = corpora.Dictionary(data_words_bigrams)
	text = data_words_bigrams
	corpus = [id2word.doc2bow(text) for text in data_words_bigrams]

	lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
	                                           id2word=id2word,
	                                           num_topics=NUM_TOPICS, 
	                                           random_state=random_state,
	                                           update_every=update_every,
	                                           chunksize=chunksize,
	                                           passes=passes,
	                                           alpha=alpha,
	                                           per_word_topics=per_word_topics,
	                                           iterations = iterations)

	coherence_model_lda = CoherenceModel(model=lda_model, texts=data_words_bigrams, dictionary=id2word, coherence='c_v')
	coherence_lda = coherence_model_lda.get_coherence()
	# print('\nCoherence Score with ' + str(NUM_TOPICS) + ' topics and ' + str(iterations)  + ' iterations: ' + str(coherence_lda))
	
	return [lda_model, coherence_lda]


def ldaMulticore(corpus, workers = 1, NUM_TOPICS = 4, fechaMin = '1-1', fechaMax = '1-1',
	random_state=100, chunksize=100, passes=10, alpha='auto', per_word_topics=True,
	iterations = 50):
	
	fechaMin = fechaMin.split('-')
	fechaMax = fechaMax.split('-')

	diaMin = int(fechaMin[0])
	diaMax = int(fechaMax[0])
	
	fechaMin = datetime.datetime(2020, int(fechaMin[1]), diaMin)
	fechaMax = datetime.datetime(2020, int(fechaMax[1]), diaMax)
	
	data_words = []

	if fechaMin.month == fechaMax.month:
		corpus = corpus[meses[fechaMin.month-1]].query('dia >= @diaMin and dia <= @diaMax')

	else:
		p1 = corpus[meses[fechaMin.month-1]].query('dia >= @diaMin')
		p2 = pd.DataFrame()
		for i in range(fechaMin.month, fechaMax.month-1):
			p2 = p2.append(corpus[meses[i]])

		p3 = corpus[meses[fechaMax.month-1]].query('dia <= @diaMax')

		corpus = pd.concat([p1,p2,p3])

	arrayTokens = corpus.tokens.values
	for tweet in arrayTokens:
		d = ' '.join(tweet)
		d = nlp(d)
		data_words.append([str(t) for t in d if t.pos_ == 'ADJ' or t.pos_ == 'PROPN' or t.pos_ == 'NOUN'])


	id2word = corpora.Dictionary(data_words)
	text = data_words
	corpus = [id2word.doc2bow(text) for text in data_words]

	lda_model = gensim.models.ldamulticore.LdaMulticore(workers=workers,
											   corpus=corpus,
	                                           id2word=id2word,
	                                           num_topics=NUM_TOPICS, 
	                                           random_state=random_state,
	                                           chunksize=chunksize,
	                                           passes=passes,
	                                           alpha=alpha,
	                                           per_word_topics=per_word_topics,
	                                           iterations = iterations)

	coherence_model_lda = CoherenceModel(model=lda_model, texts=data_words, dictionary=id2word, coherence='c_v')
	coherence_lda = coherence_model_lda.get_coherence()
	print('\nCoherence Score with ' + str(NUM_TOPICS) + ' topics: ' + str(coherence_lda))
	
	return lda_model


def printLdaModel(lda_model):
	for topic in lda_model.print_topics():
		print(topic)

# scoreMax = 0
# if __name__ == '__main__':
# 	for i in range(3,50,3):
# 		for iterations in [50,100,200,300,500,1000]:
# 			for passes in [5,10]:
# 				[model, score] = lda(c, NUM_TOPICS = i, iterations = iterations, fechaMin = '6-4', fechaMax = '6-4', passes = passes)
# 				if score > scoreMax:
# 					scoreMax = score
# 					print('scoreMax: ' + str(scoreMax) + ' , topics: ' + str(i) + ' , iterations: ' + str(iterations) + ' , passes: ' + str(passes))
#12


# print(lda_model.print_topics())
# doc_lda = lda_model[corpus]