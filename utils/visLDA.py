# import JSdistance_EN_wiki as IDence
import gensim
import pyLDAvis.gensim



#load the lda model and dictionary
dictionary = gensim.corpora.Dictionary.load_from_text('wiki_en/_wordids.txt')
corpus = gensim.corpora.MmCorpus("wiki_en/corpusbow/_bow.mm")
lda = gensim.models.LdaModel.load("wiki_en/k200_lda_symetric.dict")

pyLDAvis.gensim.prepare(lda, corpus, dictionary)

# print IDence.lda.show_topics()