import JSdistance_EN_wiki as IDence
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment
from collections import Counter
import rake
# import pandas


# # ====================================================================== #
doc = "The dirty secret in the shadow of Silicon Valley t.co/yS41C4Y1SO @google @yahoo @apple nice 2 know ur doing good with ur billions!. See my FB profile"
# doc2 = "We've helped more than 1.6 million veterans and their families realize their dream of an education." 
print doc
print vaderSentiment(doc)
doc = IDence.slangCleanser(doc)

doc = IDence.strip_links(doc)
# doc2 = IDence.strip_links(doc2)
stemDoc1 = IDence.lemmatizingText(doc)
print " ".join(stemDoc1)
# stemDoc2 = IDence.lemmatizingText(doc2)
# # print stemDoc1
# # print stemDoc2
# vec_lda = IDence.countDocLDATuple(stemDoc1)
# # vec_lda2 = IDence.countDocLDA(stemDoc2);
# print vec_lda

# rake_object = rake.Rake("SmartStoplist.txt")

# keyword = rake_object.run(doc)
# print keyword
# print IDence.countDocLDA(stemDoc1)
# print "==========================================="
# print Counter(vec_lda).most_common(2)

# m1 = [0.52,0.23,0.08,0.17]
# m2 = [0.67,0.18,0.09,0.06]

# print IDence.JSD_dist(m1,m2)

# import csv


# with open('printedAllTopic60', 'a') as csvfile:
#     evaluation = csv.writer(csvfile,quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
#     evaluation.writerow([IDence.lda.print_topics(num_topics=200, num_words=60)])

# # print IDence.JSD_dist(vec_lda,vec_lda2)
# with open('testdata.manual.2009.06.14.csv') as f:
# 	tweets = f.read().splitlines()
# 	# print tweets
# for tweet in tweets:
# 	data = tweet.split(',')
# 	print data[5], vaderSentiment(data[5])
# 	with open('evaluationdata.csv', 'a') as csvfile:
# 	    evaluation = csv.writer(csvfile,quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
# 	    evaluation.writerow([data[5],data])
# # print IDence.sentiClass("really bad performance poor you :(")

# print IDence.lda.show_topics()
