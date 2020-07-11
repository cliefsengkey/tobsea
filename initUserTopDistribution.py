#!/usr/bin/env python
# encoding: utf-8

import utils.JSdistance_EN_wiki as cs
import os
import errno
import re
import collections
from collections import Counter
import heapq
# import ScraperTweet as sc
import RAKE
import operator
import wikipedia as wiki
import csv
import random
import json

DIR = 'datasets'

def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occured

def userProfilingLDA(screen_name):

	userDict = {}

	with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+screen_name+'_followers.txt') as f:
		followers = f.read().splitlines()

	for user in followers:
		# if os.path.exists(str(DIR)+'/'+str(screen_name)+'_datasets/'+ str(user) +'/'+ str(user) +'_UserProfilingLDA.json'):
		# 	print "pass"
		# 	continue
		# with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'.txt') as f:
		# 	all_tweets = f.read().splitlines()

		# if len(all_tweets) >= 15:
		# 	print "pass", user
		# 	continue
		# else:
		# 	silentremove(str(DIR)+'/'+str(screen_name)+'_datasets/'+ str(user) +'/'+ str(user) +'_UserProfilingLDA.json')

		print 'initiating for: ', user

		#User profile description relevance. capture user profile desciption start here:
		if os.path.exists(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'_desc_followers.txt'):
			with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'_desc_followers.txt') as f:
				_desc_followers = f.read()
				_desc_followers = cs.slangCleanser(_desc_followers)
				_desc_followers = cs.lemmatizingText(_desc_followers)
				_desc_followers = cs.countDocLDA(_desc_followers)
		else:
			_desc_followers = ""

		#count Recent Hashtag tweets Score start here:
		if os.path.exists(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'_hashtags_tweets.txt'):
			with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'_hashtags_tweets.txt') as f:
				hashtags_tweets = f.read()
				hashtags_tweets = cs.slangCleanser(hashtags_tweets)
				hashtags_tweets = cs.lemmatizingText(hashtags_tweets)
				hashtags_tweets = cs.countDocLDA(hashtags_tweets)
		else:
			hashtagsInterest = 0
			hashtags_tweets = ""


		#count Recent Tweets Score start here:
		if os.path.exists(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'.txt'):
			with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'.txt') as f:
				all_tweets = f.read().splitlines()
				if len(all_tweets) > 1:
					all_tweets = " ".join(all_tweets)
					all_tweets = cs.slangCleanser(all_tweets)
					all_tweets = cs.lemmatizingText(all_tweets)
					all_tweets = cs.countDocLDA(all_tweets)


		else:
			all_tweets = ""
			continue


		#count recent Retweet Score start here:
		if os.path.exists(str(DIR)+'/'+str(screen_name)+'_datasets/'+ str(user) +'/'+ str(user) +'_retweets.txt'):
			with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+ str(user) +'/'+ str(user) +'_retweets.txt') as f:
				all_per_tweet = f.read()
				all_per_tweet = cs.slangCleanser(all_per_tweet)
				all_per_tweet = cs.lemmatizingText(all_per_tweet)
				all_per_tweet = cs.countDocLDA(all_per_tweet)


			with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+ str(user) +'/'+ str(user) +'_retweets.txt') as f:
				num_rt = len(f.read().splitlines())
		else:
			all_per_tweet = ""
			rt_tweets = 0
			num_rt = 0


		#count number of follower Score start here:
		if os.path.exists(str(DIR)+'/'+str(screen_name)+'_datasets/'+ str(user) +'/'+ str(user) +'_count_followers.txt'):
			with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+ str(user) +'/'+ str(user) +'_count_followers.txt') as f:

				num_followers = f.read().replace('\n', ' ')
		else:
			num_followers = 0


		userDict['profile'] = _desc_followers
		userDict['hashtag'] = hashtags_tweets
		userDict['recent'] = all_tweets
		userDict['sharing'] = all_per_tweet
		userDict['num_rt'] = num_rt
		userDict['num_followers'] = num_followers

		if os.path.exists(str(DIR)+'/'+str(screen_name)+'_datasets/'+ str(user) +'/'+ str(user) +'_UserProfilingLDA.json'):
			silentremove(str(DIR)+'/'+str(screen_name)+'_datasets/'+ str(user) +'/'+ str(user) +'_UserProfilingLDA.json')

		with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+ str(user) +'/'+ str(user) +'_UserProfilingLDA.json', 'w') as fp:
		    json.dump(userDict, fp)

def userProfilingSentiment(screen_name):

	with open('testingdata_tweet.txt') as f:
		tweets = f.read().splitlines()

		for new_tweet in tweets:
			sentiClassA = cs.sentiClass(new_tweet)

			rake_object = RAKE.Rake("SmartStoplist.txt")
			wiki.set_lang("en")

			keyword = rake_object.run(new_tweet)
			# print keyword
			# print wiki.summary(str(keyword[0][0])).encode("utf-8")

			try :
				summ_wiki = wiki.summary(str(keyword[0][0])).encode("utf-8")
			except wiki.exceptions.PageError:
				try:
					if keyword[1][1] and keyword[1][1] > 1:
						summ_wiki = wiki.summary(str(keyword[1][0])).encode("utf-8")
				except wiki.exceptions.PageError:
					summ_wiki = str(keyword[1][0])
				aug_tweet = new_tweet.encode('utf-8') + " " + summ_wiki

			else :
				aug_tweet = new_tweet.encode('utf-8') + " " + summ_wiki

			print '\nevaluateSimilarity for tweet:', aug_tweet

			# preprocessed_msg = cs.slangCleanser(aug_tweet)
			preprocessed_msg = cs.slangCleanser(new_tweet)
			preprocessed_msg = cs.lemmatizingText(preprocessed_msg)
			ldaScoreA = cs.countDocLDA(preprocessed_msg)

			userDict = {}

			with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+screen_name+'_followers.txt') as f:
				followers = f.read().splitlines()

			for user in followers:
				
				print 'initiating for: ', user

				#count Recent Tweets Score start here:
				if os.path.exists(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'.txt'):
					#sentiment score features
					"Open file again for sentiment based"
					with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'.txt') as f:

						data_tweets = f.read().splitlines()
						sentiScore = cs.sentiInterest(data_tweets,ldaScoreA,sentiClassA)
						sentiInterest = cs.sentiInterest(data_tweets,ldaScoreA,sentiClassA)
						if sentiInterest > 0.1:
							dct["msg"+str(index)].append(user)

				else:
					continue

				if os.path.exists(str(DIR)+'/'+str(screen_name)+'_datasets/'+ str(user) +'/'+ str(user) +'_UserProfilingSentiment.csv'):
					silentremove(str(DIR)+'/'+str(screen_name)+'_datasets/'+ str(user) +'/'+ str(user) +'_UserProfilingSentiment.csv')


			with open('Clustering_UserSentiment_perMsg.csv', 'a') as csvfile:
				evaluation = csv.writer(csvfile,quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
				evaluation.writerow([new_tweet,dct["msg"+str(index)]])

def countTweets(screen_name):

	userDict = {}
	totalTweets = 0;

	with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+screen_name+'_followers.txt') as f:
		followers = f.read().splitlines()

	for user in followers:
		print 'counting tweets of: ', user


		#count Recent Hashtag tweets Score start here:
		if os.path.exists(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'_hashtags_tweets.txt'):
			with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'_hashtags_tweets.txt') as f:
				hashtags_tweets = f.read().splitlines()
				totalTweets += len(hashtags_tweets)


		#count Recent Tweets Score start here:
		if os.path.exists(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'.txt'):
			with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'.txt') as f:
				all_tweets = f.read().splitlines()
				totalTweets += len(all_tweets)

		print 'Total tweets of: '+screen_name,totalTweets

		if os.path.exists(str(screen_name)+'_datasets/totalTweets'+str(screen_name)+'.txt'):
			silentremove(str(screen_name)+'_datasets/totalTweets.txt')

		with open(str(screen_name)+'_datasets/totalTweets'+str(screen_name)+'.txt', 'w') as fp:
		    fp.write("Total tweets: %s" % totalTweets)
		    fp.close


def userProfilingLDAManual(screen_name,user):

	userDict = {}

	if os.path.exists(str(DIR)+'/'+str(screen_name)+'_datasets/'+ str(user) +'/'+ str(user) +'_UserProfilingLDA.json'):
		silentremove(str(DIR)+'/'+str(screen_name)+'_datasets/'+ str(user) +'/'+ str(user) +'_UserProfilingLDA.json')

	print user

	#User profile description relevance. capture user profile desciption start here:
	if os.path.exists(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'_desc_followers.txt'):
		with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'_desc_followers.txt') as f:
			_desc_followers = f.read()
			_desc_followers = cs.slangCleanser(_desc_followers)
			_desc_followers = cs.lemmatizingText(_desc_followers)
			_desc_followers = cs.countDocLDA(_desc_followers)
	else:
		_desc_followers = ""

	#count Recent Hashtag tweets Score start here:
	if os.path.exists(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'_hashtags_tweets.txt'):
		with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'_hashtags_tweets.txt') as f:
			hashtags_tweets = f.read()
			hashtags_tweets = cs.slangCleanser(hashtags_tweets)
			hashtags_tweets = cs.lemmatizingText(hashtags_tweets)
			hashtags_tweets = cs.countDocLDA(hashtags_tweets)
	else:
		hashtagsInterest = 0
		hashtags_tweets = ""


	#count Recent Tweets Score start here:
	if os.path.exists(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'.txt'):
		with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'.txt') as f:
			all_tweets = f.read().splitlines()
			if len(all_tweets) >= 15:
				all_tweets = " ".join(all_tweets)
				all_tweets = cs.slangCleanser(all_tweets)
				all_tweets = cs.lemmatizingText(all_tweets)
				all_tweets = cs.countDocLDA(all_tweets)

			else:
				all_tweets = ""


	#count recent Retweet Score start here:
	if os.path.exists(str(DIR)+'/'+str(screen_name)+'_datasets/'+ str(user) +'/'+ str(user) +'_retweets.txt'):
		with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+ str(user) +'/'+ str(user) +'_retweets.txt') as f:
			all_per_tweet = f.read()
			all_per_tweet = cs.slangCleanser(all_per_tweet)
			all_per_tweet = cs.lemmatizingText(all_per_tweet)
			all_per_tweet = cs.countDocLDA(all_per_tweet)


		with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+ str(user) +'/'+ str(user) +'_retweets.txt') as f:
			num_rt = len(f.read().splitlines())
	else:
		all_per_tweet = ""
		rt_tweets = 0
		num_rt = 0


	#count number of follower Score start here:
	if os.path.exists(str(DIR)+'/'+str(screen_name)+'_datasets/'+ str(user) +'/'+ str(user) +'_count_followers.txt'):
		with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+ str(user) +'/'+ str(user) +'_count_followers.txt') as f:

			num_followers = f.read().replace('\n', ' ')
	else:
		num_followers = 0


	userDict['profile'] = _desc_followers
	userDict['hashtag'] = hashtags_tweets
	userDict['recent'] = all_tweets
	userDict['sharing'] = all_per_tweet
	userDict['num_rt'] = num_rt
	userDict['num_followers'] = num_followers

	with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+ str(user) +'/'+ str(user) +'_UserProfilingLDA.json', 'w') as fp:
	    json.dump(userDict, fp)


if __name__ == '__main__':

	# userProfilingLDAManual('IDenceFinder','PAPs_ID')
	
	# user_dataset = ['Europ4Americans','WillSmirk4Food','realsusandixon','AJMoz19','IDenceFinder','whussupfoot','valmaidearden','Todd_The_Fox','daniellejade198']
	# user_dataset = ['HazelCowie','thewhiterobin','MinniesMaison']
	user_dataset = ['AbilityNYU','DrRickPiet','Rafael_mstud','_what_a_pain','iamchrissmith','pberendt','AlecEllin','DreamerBuckeye',
	'SamScoopCooper','aarthikaran','jacobdudzinski','ryansford','AletheaMB','GTWhovian','ShoshiBee16','adamsohn','jaimelasticity',
	'somtonweke4','AlexisConfer','GimpGirl64','SmartCitiesL','anndavisgarvin','jesterthejedi','steeltoedocs','Alexus1436',
	'HBUWSoccer','SophieYVE','belovedbless','kaity_wong','talinrae','AliceHeart1553','HeroinLover','SvengalAmy','bethpitch',
	'kirstenarlee','teachtoreachme','AllTechIsHuman','JLPaniaguaValle','TashaSimmers','caroline_havard','kyriariel','thahitun',
	'AuditYourBrand','Julia_suarezz','ThCornbreadHour','cheyenne7733','lanchic1m','thanksaiko','Blockcampio','LaurenAvila21',
	'TheBirdLeaf1','danielone','laneykimble24','tmamut','Cabe_Parham','LiatSpiro','TreyFaulkner39','doc_strategy','lo7hughes',
	'tuanpmt','Cat_Elwonger','MariaSemykoz','TwittleyJules','e_klymenko','loiscar41770093','upsofdowns21','D1defender13',
	'MechAero2019','UAHouseDavos','emaniintl','madibissa','vietlq','Danny_Kad','PersonsAssetCL','VisibilityToday','emzbox',
	'mawillits','wife_stretford','DoBetterTV','RPA_BizDev','YVyTruong','haleyottem','mfoxmck']

	for user in user_dataset:
		print "profiling on ",user
		print "============================::"
		userProfilingLDA(user)
		# userProfilingSentiment(user)