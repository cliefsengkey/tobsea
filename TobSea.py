#!/usr/bin/env python
# encoding: utf-8

"""
	User basic information:
		print ("Basic information for", user.name)
		print ("Screen Name:", user.screen_name)
		print ("Name: ", user.name)
		print ("Twitter Unique ID: ", user.id)
		print ("Account created at: ", user.created_at)

	Tweepy tweets attribute:
	    print ("ID:", tweet.id)
        print ("User ID:", tweet.user.id)
        print ("Text:", tweet.text)
        print ("Created:", tweet.created_at)
        print ("Geo:", tweet.geo)
        print ("Contributors:", tweet.contributors)
        print ("Coordinates:", tweet.coordinates) 
        print ("Favorited:", tweet.favorited)
        print ("In reply to screen name:", tweet.in_reply_to_screen_name)
        print ("In reply to status ID:", tweet.in_reply_to_status_id)
        print ("In reply to status ID str:", tweet.in_reply_to_status_id_str)
        print ("In reply to user ID:", tweet.in_reply_to_user_id)
        print ("In reply to user ID str:", tweet.in_reply_to_user_id_str)
        print ("Place:", tweet.place)
        print ("Retweeted:", tweet.retweeted)
        print ("Retweet count:", tweet.retweet_count)
        print ("Source:", tweet.source)
        print ("Truncated:", tweet.truncated)
"""
import utils.JSdistance_EN_wiki as cs
import os
import errno
import re
import collections
from collections import Counter
import heapq
import utils.ScraperTweet as sc
import RAKE
import operator
import wikipedia as wiki
import csv
import random
import json
import ast

DIR = 'datasets'
RESULT_PATH = "RESULTS"

if not os.path.exists(RESULT_PATH):
    os.makedirs(RESULT_PATH)

stoplist_file = "utils/SmartStoplist.txt"

def keywordExtension(new_tweet):
	rake_object = RAKE.Rake(stoplist_file)
	wiki.set_lang("en")

	keyword = rake_object.run(new_tweet)

	try :
		summ_wiki = wiki.summary(str(keyword[0][0])).encode("utf-8")

		print wiki.summary(str(keyword[1][0])).encode("utf-8")
	except wiki.exceptions.PageError:
		try:
			if keyword[1][1] and keyword[1][1] > 1:
				summ_wiki = wiki.summary(str(keyword[1][0])).encode("utf-8")

				print wiki.summary(str(keyword[1][0])).encode("utf-8")
		except wiki.exceptions.PageError:
			summ_wiki = str(keyword[1][0])
		aug_tweet = new_tweet.encode('utf-8') + " " + summ_wiki

	else :
		aug_tweet = new_tweet.encode('utf-8') + " " + summ_wiki
	print '\nevaluateSimilarity for tweet:', aug_tweet


def evaluateSimilarityJSON(screen_name,new_tweet):

	sentiClassA = cs.sentiClass(new_tweet)

	rake_object = RAKE.Rake(stoplist_file)
	wiki.set_lang("en")

	keyword = rake_object.run(new_tweet)
	# print keyword
	# print wiki.summary(str(keyword[0][0])).encode("utf-8")

	# try :
	# 	summ_wiki = wiki.summary(str(keyword[0][0])).encode("utf-8")
	# except (wiki.exceptions.PageError,wiki.exceptions.DisambiguationError) as e:
	# 	try:
	# 		if keyword[1][1] and keyword[1][1] > 1:
	# 			summ_wiki = wiki.summary(str(keyword[1][0])).encode("utf-8")
	# 	except (wiki.exceptions.PageError,wiki.exceptions.DisambiguationError) as e:
	# 		summ_wiki = str(keyword[1][0])
	# 	aug_tweet = new_tweet.encode('utf-8') + " " + summ_wiki
	# else :
	# 	aug_tweet = new_tweet.encode('utf-8') + " " + summ_wiki

	# print '\nevaluateSimilarity for tweet:', aug_tweet

	# preprocessed_msg = cs.slangCleanser(aug_tweet)
	preprocessed_msg = cs.slangCleanser(new_tweet)
	preprocessed_msg = cs.lemmatizingText(preprocessed_msg)
	ldaScoreA = cs.countDocLDA(preprocessed_msg)

	with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+screen_name+'_followers.txt') as f:
		followers = f.read().splitlines()

	tweet_counter = 0
	recommendation_list = collections.defaultdict(list)
	recommendation_list_np = collections.defaultdict(list)
	recommendation_list_recent = collections.defaultdict(list)
	recommendation_list_rt = collections.defaultdict(list)
	recommendation_list_hashtag = collections.defaultdict(list)
	recommendation_list_senti = collections.defaultdict(list)
	recommendation_list_prof = collections.defaultdict(list)

	recommendation_list_c = collections.defaultdict(list)

	recommendation_list_fnr = collections.defaultdict(list)
	recommendation_list_csi = collections.defaultdict(list)
	recommendation_list_cb = collections.defaultdict(list)
	recommendation_list_eb = collections.defaultdict(list)

	for user in followers:
		if os.path.exists(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'.txt'):
			with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'.txt') as f:
				all_tweets = f.read().splitlines()

		if len(all_tweets) < 2:
			print "pass", user
			continue

		print 'estimating for user: ', user

		if os.path.exists(str(DIR)+'/'+str(screen_name)+'_datasets/'+ str(user) +'/'+ str(user) +'_UserProfilingLDA.json'):

			with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+ str(user) +'/'+ str(user) +'_UserProfilingLDA.json') as json_data:
				d = json.load(json_data)

				#User profile description relevance. capture user profile desciption start here:
				if d['profile'] != "":
					profileInterest = 1-cs.JSD_dist(d['profile'],ldaScoreA)
				else:
					profileInterest = 0

				#count Recent Hashtag tweets Score start here:
				if d['hashtag'] != "":
					hashtagsInterest = 1-cs.JSD_dist(d['hashtag'],ldaScoreA) 
				else:
					hashtagsInterest = 0


				#count Recent Tweets Score start here:
				if d['recent'] != "":
					recentInterest = 1-cs.JSD_dist(d['recent'],ldaScoreA) 

					if os.path.exists(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'.txt'):
						#sentiment score features
						"Open file again for sentiment based"
						with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'.txt') as f:

							data_tweets = f.read().splitlines()
							sentiScore = cs.sentiInterest(data_tweets,ldaScoreA,sentiClassA)
							sentiInterest = cs.sentiInterest(data_tweets,ldaScoreA,sentiClassA)

						"Open file for EAR cosine_sim"
						with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'.txt') as f:

							aggregate_tweets = f.read().replace('\n', ' ')
							cosine_sim = cs.cosine_sim(new_tweet,aggregate_tweets)
				else:
					recentInterest = 0
					continue


				#count recent Retweet Score start here:
				if d['sharing'] != "":

					sharingInt = 1-cs.JSD_dist(d['sharing'],ldaScoreA) 
					num_rt = int(d['num_rt'])

				else:
					sharingInt = 0
					num_rt = 0


				#count number of follower Score start here:

				num_followers = int(d['num_followers'])
				empirical_based = num_followers*(cosine_sim*int(num_rt))


				CSI = (0.4*(recentInterest)) + (0.3*(sharingInt)) + (0.3*(hashtagsInterest))
				Topic_based = (0.25*(recentInterest)) + (0.2*(sharingInt)) + (0.2*(hashtagsInterest) + (0.15*(profileInterest)))

				#If new tweet polarity is neutral, don’t consider sentiment feature 

				#If new tweet polarity is neutral, don’t consider sentiment feature 
				if sentiClassA == "NEUTRAL":
					sentiScore = 0
				SeAT = Topic_based + (0.25*sentiScore)
				SeAT_NP = CSI + sentiScore
				# print 'SeAT: ', SeAT,'; recentInterest: ', recentInterest,'; sharingInt: ', sharingInt,'; hashtagsInterest: ', hashtagsInterest,'; profileInterest: ', profileInterest,'; sentiInterest: ', sentiInterest
				print "--------\n"
				recommendation_list[user].append(SeAT)
				recommendation_list_np[user].append(SeAT_NP)
				recommendation_list_recent[user].append(recentInterest)
				recommendation_list_rt[user].append(sharingInt)
				recommendation_list_hashtag[user].append(hashtagsInterest)
				recommendation_list_senti[user].append(sentiInterest)
				recommendation_list_prof[user].append(profileInterest)

				recommendation_list_csi[user].append(CSI)
				recommendation_list_fnr[user].append(num_followers)
				recommendation_list_eb[user].append(empirical_based)


	# Proposed System
	top_15_SeAT = heapq.nlargest(15, recommendation_list, key=recommendation_list.get)
	top_15_SeAT_NP = heapq.nlargest(15, recommendation_list_np, key=recommendation_list.get)
	top_15_rt = heapq.nlargest(15, recommendation_list_rt, key=recommendation_list_rt.get)
	top_15_hashtag = heapq.nlargest(15, recommendation_list_hashtag, key=recommendation_list_hashtag.get)
	top_15_senti = heapq.nlargest(15, recommendation_list_senti, key=recommendation_list_senti.get)
	top_15_prof = heapq.nlargest(15, recommendation_list_prof, key=recommendation_list_prof.get)
	top_15_recent = heapq.nlargest(15, recommendation_list_recent, key=recommendation_list_recent.get)

	top_15_csi = heapq.nlargest(15, recommendation_list_csi, key=recommendation_list_csi.get)
	top_15_fnr = heapq.nlargest(15, recommendation_list_fnr, key=recommendation_list_fnr.get)
	top_15_eb = heapq.nlargest(15, recommendation_list_eb, key=recommendation_list_eb.get)

	with open(str(RESULT_PATH)+'/result_'+str(screen_name)+'.csv', 'a') as csvfile:
	    evaluation = csv.writer(csvfile,quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
	    evaluation.writerow([new_tweet,top_15_SeAT,top_15_SeAT_NP,top_15_csi,top_15_eb,top_15_fnr,top_15_recent,top_15_rt,top_15_hashtag,top_15_senti,top_15_prof])



def aug_messages(new_tweet):

	sentiClassA = cs.sentiClass(new_tweet)

	rake_object = RAKE.Rake(stoplist_file)
	wiki.set_lang("en")

	keyword = rake_object.run(new_tweet)


	try :
		summ_wiki = wiki.summary(str(keyword[0][0])).encode("utf-8")
	except (wiki.exceptions.PageError,wiki.exceptions.DisambiguationError) as e:
		try:
			if keyword[1][1] and keyword[1][1] > 1:
				summ_wiki = wiki.summary(str(keyword[1][0])).encode("utf-8")
		except (wiki.exceptions.PageError,wiki.exceptions.DisambiguationError) as e:
			summ_wiki = str(keyword[1][0])
		aug_tweet = new_tweet.encode('utf-8') + " " + summ_wiki
	else :
		aug_tweet = new_tweet.encode('utf-8') + " " + summ_wiki

	print '\nevaluateSimilarity for tweet:', aug_tweet
	with open(str(RESULT_PATH)+'/messages_list.csv', 'a') as csvfile:
	    evaluation = csv.writer(csvfile,quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
	    evaluation.writerow([aug_tweet])

def evaluateSimilarity(screen_name,new_tweet):

	sentiClassA = cs.sentiClass(new_tweet)

	rake_object = RAKE.Rake(stoplist_file)
	wiki.set_lang("en")

	keyword = rake_object.run(new_tweet)
	# print keyword
	# print wiki.summary(str(keyword[0][0])).encode("utf-8")

	try :
		summ_wiki = wiki.summary(str(keyword[0][0])).encode("utf-8")
	except (wiki.exceptions.PageError,wiki.exceptions.DisambiguationError) as e:
		try:
			if keyword[1][1] and keyword[1][1] > 1:
				summ_wiki = wiki.summary(str(keyword[1][0])).encode("utf-8")
		except (wiki.exceptions.PageError,wiki.exceptions.DisambiguationError) as e:
			summ_wiki = str(keyword[1][0])
		aug_tweet = new_tweet.encode('utf-8') + " " + summ_wiki

	else :
		aug_tweet = new_tweet.encode('utf-8') + " " + summ_wiki

	print '\nevaluateSimilarity for tweet:', aug_tweet

	# preprocessed_msg = cs.slangCleanser(aug_tweet)
	preprocessed_msg = cs.slangCleanser(new_tweet)
	preprocessed_msg = cs.lemmatizingText(preprocessed_msg)
	ldaScoreA = cs.countDocLDA(preprocessed_msg)

	with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+screen_name+'_followers.txt') as f:
		followers = f.read().splitlines()

	tweet_counter = 0
	recommendation_list = collections.defaultdict(list)
	recommendation_list_recent = collections.defaultdict(list)
	recommendation_list_rt = collections.defaultdict(list)
	recommendation_list_hashtag = collections.defaultdict(list)
	recommendation_list_senti = collections.defaultdict(list)
	recommendation_list_prof = collections.defaultdict(list)

	recommendation_list_c = collections.defaultdict(list)

	recommendation_list_fnr = collections.defaultdict(list)
	recommendation_list_csi = collections.defaultdict(list)
	recommendation_list_cb = collections.defaultdict(list)
	recommendation_list_eb = collections.defaultdict(list)

	for user in followers:
		if os.path.exists(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'.txt'):
			with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'.txt') as f:
				all_tweets = f.read().splitlines()

		if len(all_tweets) < 1:
			print "pass", user
			continue

		print 'estimating for user: ', user

		if os.path.exists(str(DIR)+'/'+str(screen_name)+'_datasets/'+ str(user) +'/'+ str(user) +'_UserProfilingLDA.json'):

			with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+ str(user) +'/'+ str(user) +'_UserProfilingLDA.json') as json_data:
				d = json.load(json_data)

				#User profile description relevance. capture user profile desciption start here:
				if d['profile'] != "":
					profileInterest = cs.JSD_dist(d['profile'],ldaScoreA)
				else:
					profileInterest = 0

				#count Recent Hashtag tweets Score start here:
				if d['hashtag'] != "":
					hashtagsInterest = cs.JSD_dist(d['hashtag'],ldaScoreA) 
				else:
					hashtagsInterest = 0


				#count Recent Tweets Score start here:
				if d['recent'] != "":
					recentInterest = cs.JSD_dist(d['recent'],ldaScoreA) 

					if os.path.exists(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'.txt'):
						#sentiment score features
						"Open file again for sentiment based"
						with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'.txt') as f:

							data_tweets = f.read().splitlines()
							sentiScore = cs.sentiInterest(data_tweets,ldaScoreA,sentiClassA)
							sentiInterest = cs.sentiInterest(data_tweets,ldaScoreA,sentiClassA)

						"Open file for EAR cosine_sim"
						with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'.txt') as f:

							aggregate_tweets = f.read().replace('\n', ' ')
							cosine_sim = cs.cosine_sim(new_tweet,aggregate_tweets)
				else:
					recentInterest = 0
					continue


				#count recent Retweet Score start here:
				if d['sharing'] != "":

					sharingInt = cs.JSD_dist(d['sharing'],ldaScoreA) 
					num_rt = int(d['num_rt'])

				else:
					sharingInt = 0
					num_rt = 0


				#count number of follower Score start here:

				num_followers = int(d['num_followers'])
				empirical_based = num_followers*(cosine_sim*int(num_rt))


				CSI = (0.4*(recentInterest)) + (0.3*(sharingInt)) + (0.3*(hashtagsInterest))
				Topic_based = (0.25*(recentInterest)) + (0.2*(sharingInt)) + (0.2*(hashtagsInterest) + (0.15*(profileInterest)))

				#If new tweet polarity is neutral, don’t consider sentiment feature 
				if sentiClassA == "NEUTRAL":
					sentiScore = 0
				SeAT = Topic_based + (0.25*sentiScore)
				SeAT_NP = CSI + sentiScore
				print 'SeAT: ', SeAT,'; recentInterest: ', recentInterest,'; sharingInt: ', sharingInt,'; hashtagsInterest: ', hashtagsInterest,'; profileInterest: ', profileInterest,'; sentiInterest: ', sentiInterest
				print "\n"
				recommendation_list[user].append(SeAT)
				recommendation_list[user].append(SeAT_NP)
				recommendation_list_recent[user].append(recentInterest)
				recommendation_list_rt[user].append(sharingInt)
				recommendation_list_hashtag[user].append(hashtagsInterest)
				recommendation_list_senti[user].append(sentiInterest)
				recommendation_list_prof[user].append(profileInterest)

				recommendation_list_csi[user].append(CSI)
				recommendation_list_fnr[user].append(num_followers)
				recommendation_list_eb[user].append(empirical_based)


	# Proposed System
	top_15_SeAT = heapq.nlargest(15, recommendation_list, key=recommendation_list.get)
	top_15_SeAT_NP = heapq.nlargest(15, recommendation_list_np, key=recommendation_list.get)
	top_15_rt = heapq.nlargest(15, recommendation_list_rt, key=recommendation_list_rt.get)
	top_15_hashtag = heapq.nlargest(15, recommendation_list_hashtag, key=recommendation_list_hashtag.get)
	top_15_senti = heapq.nlargest(15, recommendation_list_senti, key=recommendation_list_senti.get)
	top_15_prof = heapq.nlargest(15, recommendation_list_prof, key=recommendation_list_prof.get)
	top_15_recent = heapq.nlargest(15, recommendation_list_recent, key=recommendation_list_recent.get)

	top_15_csi = heapq.nlargest(15, recommendation_list_csi, key=recommendation_list_csi.get)
	top_15_fnr = heapq.nlargest(15, recommendation_list_fnr, key=recommendation_list_fnr.get)
	top_15_eb = heapq.nlargest(15, recommendation_list_eb, key=recommendation_list_eb.get)

	with open(str(RESULT_PATH)+'/eval_result_'+str(screen_name)+'.csv', 'a') as csvfile:
	    evaluation = csv.writer(csvfile,quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
	    evaluation.writerow([new_tweet,top_15_SeAT,top_15_SeAT_NP,top_15_csi,top_15_eb,top_15_fnr,top_15_recent,top_15_rt,top_15_hashtag,top_15_senti,top_15_prof])

def checkTweetsSenti():

	with open('extra_testingdata.txt') as f:
		tweets = f.read().splitlines()

		with open('testingdata_senti.csv', 'a') as csvfile:
			evaluation = csv.writer(csvfile,quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

			for new_tweet in tweets:
				sentiClassA = cs.sentiClass(new_tweet)
				print new_tweet, sentiClassA
		    	# evaluation.writerow([new_tweet,sentiClassA])




def count_num_tweets(screen_name):

	with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+screen_name+'_followers.txt') as f:
		followers = f.read().splitlines()

	tweet_counter = 0
	for user in followers:
		if os.path.exists(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'.txt'):
			with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'.txt') as f:
				all_tweets = f.read().splitlines()

		tweet_counter += len(all_tweets)

	return tweet_counter,len(followers)



def run_count_tweet(user_dataset):
	total_num_of_tweet = 0
	total_num_of_follower = 0

	for user in user_dataset:
		res = count_num_tweets(user)
		total_num_of_tweet += res[0]
		total_num_of_follower += res[1]
		print "\n>>",user,res

	print("total_num_of_tweet : ",total_num_of_tweet)
	print("total_num_of_follower : ",total_num_of_follower)

def run_tobsea(user_dataset):
	for user in user_dataset:
		print "\n>>",user

		#only one tweet:
		# tweet = "Honored to be the keynote speaker at the Lake County Lincoln Day Dinner tonight at 7 PM ET at St. Elijah's in Merrillville.  Always nice to go home and see old friends.  Look for pictures from the event tomorrow."
		# evaluateSimilarityJSON(user,tweet.encode('utf-8'))


		with open('extra_testingdata.txt') as f:
			tweets = f.read().splitlines()
			# print tweets
		counter = 0
		for tweet in tweets[:2]:
			# if counter > 24:
			# 	break
			print(tweet)
			# continue
			# data = tweet.split(',')
				# evaluateSimilarity('Europ4Americans',tweet)
			# if len(tweete) >= 100:
			# aug_messages(tweet.encode('utf-8'))
			evaluateSimilarityJSON(user,tweet.encode('utf-8'))

			counter += 1

if __name__ == '__main__':

	# doc = "Adobe to Acquire Frame For $500 Million in Stock --- Publishing-Software Firm Posts 96% Rise in Profit For the Second Quarter"
	# keywordExtension(doc)
	# user_dataset = ['IDenceFinder','WillSmirk4Food','realsusandixon','AJMoz19','Europ4Americans']
	# user_dataset = ['HazelCowie','thewhiterobin','MinniesMaison','WillSmirk4Food','realsusandixon','AJMoz19','IDenceFinder','whussupfoot','valmaidearden','Europ4Americans','Todd_The_Fox','daniellejade198']
	# user_dataset = ['Todd_The_Fox','daniellejade198']

	# user_dataset = ['Todd_The_Fox']
	# user_dataset = ['HazelCowie','thewhiterobin','MinniesMaison']

	# user_dataset = ['AbilityNYU','DrRickPiet','Rafael_mstud','_what_a_pain','iamchrissmith','pberendt','AlecEllin','DreamerBuckeye',
	# 'SamScoopCooper','aarthikaran','jacobdudzinski','ryansford','AletheaMB','GTWhovian','ShoshiBee16','adamsohn','jaimelasticity',
	# 'somtonweke4','AlexisConfer','GimpGirl64','SmartCitiesL','anndavisgarvin','jesterthejedi','steeltoedocs','Alexus1436',
	# 'HBUWSoccer','SophieYVE','belovedbless','kaity_wong','talinrae','AliceHeart1553','HeroinLover','SvengalAmy','bethpitch',
	# 'kirstenarlee','teachtoreachme','AllTechIsHuman','JLPaniaguaValle','TashaSimmers','caroline_havard','kyriariel','thahitun',
	# 'AuditYourBrand','Julia_suarezz','ThCornbreadHour','cheyenne7733','lanchic1m','thanksaiko','Blockcampio','LaurenAvila21',
	# 'TheBirdLeaf1','danielone','laneykimble24','tmamut','Cabe_Parham','LiatSpiro','TreyFaulkner39','doc_strategy','lo7hughes',
	# 'tuanpmt','Cat_Elwonger','MariaSemykoz','TwittleyJules','e_klymenko','loiscar41770093','upsofdowns21','D1defender13',
	# 'MechAero2019','UAHouseDavos','emaniintl','madibissa','vietlq','Danny_Kad','PersonsAssetCL','VisibilityToday','emzbox',
	# 'mawillits','wife_stretford','DoBetterTV','RPA_BizDev','YVyTruong','haleyottem','mfoxmck']

	user_dataset = ['AbilityNYU']

	# run_count_tweet(user_dataset)
	run_tobsea(user_dataset)

	# checkTweetsSenti()
