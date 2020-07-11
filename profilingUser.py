import utils.JSdistance_EN_wiki as IDence
from collections import Counter
import os
import csv
import RAKE
import sys
# import pandas

DIR = 'datasets'

def profiling(screen_name):
	with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+screen_name+'_followers.txt') as f:
		followers = f.read().splitlines()

	for user in followers:

		if os.path.exists(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'_desc_followers.txt'):
			with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'_desc_followers.txt') as f:
				_desc_followers = f.read()
		else:
			_desc_followers = ""

		if os.path.exists(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'.txt'):
			with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'.txt') as f:
				all_tweets = f.read()
		else:
			all_tweets = ""

		if os.path.exists(str(DIR)+'/'+str(screen_name)+'_datasets/'+ str(user) +'/'+ str(user) +'_retweets.txt'):
			with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+ str(user) +'/'+ str(user) +'_retweets.txt') as f:
				# all_per_tweet = f.read().replace('\n', ' ')
				all_per_tweet = f.read()
		else:
			all_per_tweet = ""

		aggregated = " ".join([_desc_followers, all_tweets, all_per_tweet])
		preprocessed = IDence.slangCleanser(aggregated)
		preprocessed = IDence.strip_all_entities(preprocessed)
		preprocessed = IDence.strip_links(preprocessed)
		# preprocessed = IDence.lemmatizingText(preprocessed)
		# vec_lda = IDence.countDocLDATuple(preprocessed)

		rake_object = RAKE.Rake("SmartStoplist.txt")


		keyword = rake_object.run(preprocessed)

		try:
			extract0 = keyword[0][0]
			extract1 = keyword[1][0]
			extract2 = keyword[2][0]
		except IndexError:
			extract1 = ""
			extract2 = ""


		# print user, keyword[0][0].encode(sys.stdout.encoding, errors='replace')

		with open('profiling_clean_'+str(screen_name)+'.csv', 'a') as csvfile:
			evaluation = csv.writer(csvfile,quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
			evaluation.writerow([user.encode("utf-8"), _desc_followers, extract0.encode("utf-8"), extract1.encode("utf-8"), extract2.encode("utf-8")]) 


if __name__ == '__main__':

    # user_dataset = ['daniellejade198']
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
    	profiling(user)