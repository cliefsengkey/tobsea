# before running, you need to modify ldamodel.py in gensim/models folder by adding this function into it:

#     def get_document_topics_tuple(self, bow, minimum_probability=None):
#         """
#         Return topic distribution for the given document `bow`, as a list of
#         (topic_id, topic_probability) 2-tuples.

#         Ignore topics with very low probability (below `minimum_probability`).

#         """
#         if minimum_probability is None:
#             minimum_probability = self.minimum_probability
#         minimum_probability = max(abs(minimum_probability), 1e-8)  # never allow zero values in sparse output
#         # minimum_probability = 0.0  # never allow zero values in sparse output

#         # if the input vector is a corpus, return a transformed corpus
#         is_corpus, corpus = utils.is_corpus(bow)
#         if is_corpus:
#             return self._apply(corpus)

#         gamma, _ = self.inference([bow])
#         topic_dist = gamma[0] / sum(gamma[0])  # normalize distribution
#         return [(topicid, topicvalue) for topicid, topicvalue in enumerate(topic_dist)
#         # return [topicvalue for topicid, topicvalue in enumerate(topic_dist)
#                 if topicvalue >= minimum_probability]

# =================================

# and also customize utils.py in gensim site-packages by adding this function:

# def lemmatize_no_tag(content, allowed_tags=re.compile('(NN|VB|JJ|RB)'), light=False,
#         stopwords=frozenset(), min_length=2, max_length=15):
#     """
#     This function is only available when the optional 'pattern' package is installed.

#     Use the English lemmatizer from `pattern` to extract UTF8-encoded tokens in
#     their base form=lemma, e.g. "are, is, being" -> "be" etc.
#     This is a smarter version of stemming, taking word context into account.

#     Only considers nouns, verbs, adjectives and adverbs by default (=all other lemmas are discarded).

#     >>> lemmatize('Hello World! How is it going?! Nonexistentword, 21')
#     ['world/NN', 'be/VB', 'go/VB', 'nonexistentword/NN']

#     >>> lemmatize('The study ranks high.')
#     ['study/NN', 'rank/VB', 'high/JJ']

#     >>> lemmatize('The ranks study hard.')
#     ['rank/NN', 'study/VB', 'hard/RB']

#     """
#     if not has_pattern():
#         raise ImportError("Pattern library is not installed. Pattern library is needed in order  \
#          to use lemmatize function")
#     from pattern.en import parse

#     if light:
#         import warnings
#         warnings.warn("The light flag is no longer supported by pattern.")

#     # tokenization in `pattern` is weird; it gets thrown off by non-letters,
#     # producing '==relate/VBN' or '**/NN'... try to preprocess the text a little
#     # FIXME this throws away all fancy parsing cues, including sentence structure,
#     # abbreviations etc.
#     content = u(' ').join(tokenize(content, lower=True, errors='ignore'))

#     parsed = parse(content, lemmata=True, collapse=False)
#     result = []
#     for sentence in parsed:
#         for token, tag, _, _, lemma in sentence:
#             if min_length <= len(lemma) <= max_length and not lemma.startswith('_') and lemma not in stopwords:
#                 if allowed_tags.match(tag):
#                     # put comment to remove tag after word
#                     # lemma += "/" + tag[:2]
#                     result.append(lemma.encode('utf8'))
#     return result
#	=========================

from __future__ import division
from gensim.corpora import Dictionary, HashDictionary, MmCorpus, WikiCorpus
from gensim import utils 
import numpy as np
import logging, gensim, bz2
from pprint import pprint   # pretty-printer
import timing
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#import library for preprocessing from nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.lancaster import LancasterStemmer



# #load the lda model and dictionary
# dictionary = gensim.corpora.Dictionary.load('wiki_en/_wordids.dict')
# # corpus = gensim.corpora.MmCorpus("wiki_en/_bow.mm")
# lda = gensim.models.LdaModel.load("wiki_en/lda.model")

#load the lda model and dictionary
dictionary = gensim.corpora.Dictionary.load('twitter_corpus/tweets.dict')
# corpus = gensim.corpora.MmCorpus("twitter_corpus/_bow.mm")
lda = gensim.models.LdaModel.load("twitter_corpus/tweets_lda.dict")
stop = set(stopwords.words('english'))

#step1 stemming using nltk:  removing whitespaces, punctuations, stopwords, and stemming words
def stemmingDocs(docs):

	tokenizer = RegexpTokenizer(r'\w+')

	if isinstance(docs, list):

		processed = []
		for document in docs:
		    intermediate = tokenizer.tokenize(document)
		    intermediate = [i for i in intermediate if i not in stop]
		    # FIXME: using other stemmers also to know quality of each stemmed text
		    lanste = LancasterStemmer()
		    intermediate = [lanste.stem(i) for i in intermediate]
		    processed.append(intermediate)

	else:
		intermediate = tokenizer.tokenize(docs)
		intermediate = [i for i in intermediate if i not in stop]
		lanste = LancasterStemmer()
		intermediate = [lanste.stem(i) for i in intermediate]
		processed = intermediate

	return processed


def lemmatizingDocuments(docs):
	#split a file per line and get a tweet, afterwards do lemmatizing

	raw = open(docs, 'r').read().lower().split("\n")
	docLists = []
	for doc in raw:
		data = doc.split('",')
		temp = utils.lemmatize_no_tag(data[5])
		docLists.append(temp)

	return docLists

def lemmatizingText(docs):
	#split a file per line and get a tweet, afterwards do lemmatizing

	if isinstance(docs, list):
		docLists = []
		for doc in docs:
			data = doc.split('\n')
			temp = utils.lemmatize_no_tag(data[5])
			docLists.append(temp)
	else:
		docLists = utils.lemmatize_no_tag(docs)
		docLists = [i for i in docLists if i not in stop]

	return docLists


#do lemmatizing instead of stemming (utilize pattern library, modified by gensim) and apply english stopwords in nltk
def lemmatizingText2(docs):

	#check either docs is a list or not
	if isinstance(docs, list):
		lemmatized = []
		for doc in docs:
			temp = utils.lemmatize_no_tag(doc)
			temp = [i for i in temp if i not in stop]
			lemmatized.append(temp)
	else:
		lemmatized = utils.lemmatize_no_tag(docs)
		lemmatized = [i for i in lemmatized if i not in stop]

	return lemmatized

def JSD_dist(LDA_a, LDA_b):
	# However the JSD is not a metric (hence the term divergence in its name). In particular, it does not satisfy the triangle inequality (which the Euclidean distance does). Interestingly, this defect can be rectified by replacing JSD with the square root of JSD (the JSD metric). 

	#Jensen-Shannon Distance is a standard way to measure similarity between 2 probability distribution, giving the value from 0 to 1, 0 means close, 1 means far away.
	LDA_a = np.array(LDA_a)
	LDA_b = np.array(LDA_b)
	eps = 1e-32
	M = 0.5*(LDA_a+LDA_b+eps)
	distance = np.sqrt(0.5*(np.sum(LDA_a*np.log(LDA_a/M+eps)) + np.sum(LDA_b*np.log(LDA_b/M+eps))))
	return distance



def mean(a):
	#return the average of multiple list inside list
    return sum(a) / len(a)
# print map(mean, zip(*a))

def listAvg(array):
	# zip() takes multiple iterable arguments, and returns slices of those iterables (as tuples), until one of the iterables cannot return anything more. In effect, it performs a transpose operation, akin to matrices.
	dataAvg = [float(sum(col))/len(col) for col in zip(*array)]
	return dataAvg;


def countMultipleDocLDA(stemmedDocs):

	tweetLists = []
	for tweet in stemmedDocs:
		doc_lda = countDocLDA(tweet)
		tweetLists.append(doc_lda)

	avgLDA = listAvg(tweetLists)

	return avgLDA

def stemDocuments(docs):

	raw = open(docs, 'r').read().lower().split("\n")

	docLists = []
	for doc in raw:
		data = doc.split('",')
		docLists.append(data[5])

	formated_data = lemmatizingDocs(docLists)
	return formated_data


def countDocLDA(document):

	vec_bow = dictionary.doc2bow(document)
	ldaProb = lda[vec_bow]

	return ldaProb

def countDocLDATuple(document):

	vec_bow = dictionary.doc2bow(document)
	ldaProb = lda.get_document_topics_tuple(vec_bow,minimum_probability=None)

	return ldaProb

# ====================================================================== #
doc = "watching football in the garden on saturday night come and join us";
doc2 = "playing basketball in the midnight";

stemDoc1 = lemmatizingText(doc)
stemDoc2 = lemmatizingText(doc2)
print "After lemmatizing: Doc1 =>",stemDoc1, " - -\n Doc2 => ", stemDoc2
vec_lda = countDocLDA(stemDoc1);
vec_lda2 = countDocLDA(stemDoc2);

print "\n-----------------------------------------"
print "lda with tuple:", countDocLDATuple(stemDoc2)
print "lda2 with tuple:", countDocLDATuple(stemDoc2)
print "\nWords distribution Topic #0 -----------------------------------------"
print lda.print_topic(0, topn=20)
print "\nWords distribution Topic #9 -----------------------------------------\n"
print lda.print_topic(9, topn=20)

print "-----------------------------------------\n"
# the parameters for JSD_dist is a list of probability distributions e.g. LDA_a = [0.1, 0.2, 0.2, 0.5]
dist = JSD_dist(vec_lda,vec_lda2)
print "Distance (Jensen Shannon Distance) between Doc1 and Doc2 = ", dist
print "-----------------------------------------\n"

docname = "testdata.manual.2009.06.14.csv"
stemmed = lemmatizingDocuments(docname)
doc_lda_avg = countMultipleDocLDA(stemmed)
distAll = JSD_dist(vec_lda,doc_lda_avg)
# print "AVG prob of: ",docname, " = ", doc_lda_avg
# kerasss

print "Distance (Jensen Shannon Distance) between :\n", doc ," and all tweets in this doc: \n", docname, " = ", distAll







