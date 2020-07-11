import logging, gensim, bz2
logging.basicConfig(filename='trainingLDA.log', format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import collections
import random

#load the lda model and dictionary


# load id->word mapping (the dictionary), one of the results of step 2 above
id2word = gensim.corpora.Dictionary.load_from_text('wiki_en/_wordids.txt')
# load corpus iterator
mm = gensim.corpora.MmCorpus('wiki_en/_tfidf.mm')

grid = collections.defaultdict(list)

# Choose a parameter you are wanting to search, for example num_topics or alpha / eta, make sure you substitute "parameter_value"
# into the model below instead of a static value.
#
# num topics
parameter_list=[10, 20, 30, 45, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250]

# alpha / eta
# parameter_list=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0, 1.5]

# we can sample if we like
# print "random sampling corpus..."
# cp = random.sample(corpus,522262)

# shuffle corpus
print "listing corpus..."
cp = list(corpus)
# print "shuffling corpus..."
# random.shuffle(cp)

print "split into 0.8 raining and 0.2 test sets..."
# split into 80% training and 20% test sets
p = int(len(cp) * .5)
cp_train = cp[0:p]
cp_test = cp[p:]

# for num_topics_value in num_topics_list:
for parameter_value in parameter_list:

    # print "starting pass for num_topic = %d" % num_topics_value
    print "starting pass for parameter_value = %.3f" % parameter_value
    start_time = time.time()

    # run model
    model = models.LdaMulticore(corpus=cp_train, id2word=dictionary, num_topics=parameter_value)
    # model = models.ldamodel.LdaModel(corpus=cp_train, id2word=dictionary, num_topics=parameter_value, chunksize=3125, 
    #                                 passes=25, update_every=0, alpha=None, eta=None, decay=0.5,
    #                                 distributed=True)
    


    # show elapsed time for model
    elapsed = time.time() - start_time
    print "Elapsed time: %s" % elapsed

    perplex = model.bound(cp_test)
    print "Perplexity: %s" % perplex
    grid[parameter_value].append(perplex)

    per_word_perplex = np.exp2(-perplex / sum(cnt for document in cp_test for _, cnt in document))
    print "Per-word Perplexity: %s" % per_word_perplex
    grid[parameter_value].append(per_word_perplex)