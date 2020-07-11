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
import utils.ScraperTweet as sc
import operator
import csv
import random
import collections
from collections import Counter
from collections import defaultdict
import ast

THRESHOLD = 0.6

DIR = 'datasets'

def clusterInterest(screen_name):
	
	dct = defaultdict(list)
	for i in xrange(200):
	    dct["topic{}".format(i)]

	with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+screen_name+'_followers.txt') as f:
		followers = f.read().splitlines()

	tweet_counter = 0

	for user in followers:
		print user

		if os.path.exists(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'_hashtags_tweets.txt'):
			with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'_hashtags_tweets.txt') as f:
				hashtags_tweets = f.read()

				f.close()
		else:
			hashtags_tweets = ""

		#count recent Retweet Score start here:
		if os.path.exists(str(DIR)+'/'+str(screen_name)+'_datasets/'+ str(user) +'/'+ str(user) +'_retweets.txt'):
			with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+ str(user) +'/'+ str(user) +'_retweets.txt') as f:
				all_per_tweet = f.read()

				f.close()

		else:
			all_per_tweet = ""

		#User profile description relevance. capture user profile desciption start here:
		if os.path.exists(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'_desc_followers.txt'):
			with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'_desc_followers.txt') as f:
				_desc_followers = f.read()
		else:
			_desc_followers = ""

		#count Recent Tweets Score start here:
		if os.path.exists(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'.txt'):
			with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'.txt') as f:
				all_tweets = f.read().splitlines()
				all_tweets.append(str(_desc_followers))
				all_tweets.append(str(hashtags_tweets))
				all_tweets.append(str(all_per_tweet))

				all_tweets = " ".join(all_tweets)
				# print all_tweets
				all_tweets = cs.slangCleanser(all_tweets)
				all_tweets = cs.lemmatizingText(all_tweets)
				ldaScore = cs.countDocLDATuple(all_tweets)
				for topic in ldaScore:
					if topic[1] > 0.1:
						dct["topic"+str(topic[0])].append(user)


	#store all collections to file
	print '\n'
	with open('clusteringFollowersOf_'+screen_name+'.csv', 'a') as csvfile:
		evaluation = csv.writer(csvfile,quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
		for j in range(200):
			evaluation.writerow([j,dct["topic"+str(j)]])

def mergeAllCluster(user_dataset):
	
	dct = defaultdict(list)
	for i in xrange(200):
	    dct["topic{}".format(i)]
	
	for user in user_dataset:
		print user

		with open('clusteringFollowersOf_'+user+'.csv','rb') as f:
			data = csv.reader(f,delimiter=',',quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
			for row in data:
				temp = ast.literal_eval(row[1])
				dct["topic"+str(row[0])].append(temp)
	#store all collections to file
	print '\n'
	with open('mergeAllCluster_new_data.csv', 'a') as csvfile:
		evaluation = csv.writer(csvfile,quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
		for j in range(200):
			mergeList = sum(dct["topic"+str(j)], [])
			evaluation.writerow([j,mergeList])

def merge2FilesLists(files):
	
	dct = defaultdict(list)
	for i in xrange(200):
	    dct["topic{}".format(i)]
	
	for file_ in files:
		print file_

		with open(file_+'.csv','rb') as f:
			data = csv.reader(f,delimiter=',',quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
			for row in data:
				temp = ast.literal_eval(row[1])
				dct["topic"+str(row[0])].append(temp)
	#store all collections to file
	print '\n'
	with open('mergeAllCluster_10accounts.csv', 'a') as csvfile:
		evaluation = csv.writer(csvfile,quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
		for j in range(200):
			mergeList = sum(dct["topic"+str(j)], [])
			evaluation.writerow([j,mergeList])


if __name__ == '__main__':

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
	

	#STEP BY STEP
	"""
		INITIAL STEP: PLEASE LIST ALL USERNAME IN A LIST TO BE USED AS INPUT OF THE FUNCTION

		1. Clustering each user topic interest using function 'clusterInterest(input)' input paramater is the list of user in datasets folder
		2. After clustering, run mergeAllCluster(input) the input is also the same, i.e. all user dataset
		3. Run this python file by executing on your terminal: python 1_clusteringFriendInterest.py
	"""

	#1
	for user in user_dataset:
		print user
		clusterInterest(user)
	#2
	mergeAllCluster(user_dataset)

	# clusterInterest('daniellejade198')
