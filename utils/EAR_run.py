
DIR = 'Total_83users'

def evaluateSimilarityJSON(screen_name,new_tweet):

	sentiClassA = cs.sentiClass(new_tweet)

	rake_object = rake.Rake("SmartStoplist.txt")
	wiki.set_lang("en")

	keyword = rake_object.run(new_tweet)
	preprocessed_msg = cs.slangCleanser(new_tweet)
	preprocessed_msg = cs.lemmatizingText(preprocessed_msg)
	ldaScoreA = cs.countDocLDA(preprocessed_msg)

	with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+screen_name+'_followers.txt') as f:
		followers = f.read().splitlines()

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


				#count Recent Tweets Score start here:
				if d['recent'] != "":
					recentInterest = 1-cs.JSD_dist(d['recent'],ldaScoreA) 

					if os.path.exists(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'.txt'):
						"Open file for EAR cosine_sim"
						with open(str(DIR)+'/'+str(screen_name)+'_datasets/'+str(user)+'/'+ str(user) +'.txt') as f:

							aggregate_tweets = f.read().replace('\n', ' ')
							cosine_sim = cs.cosine_sim(new_tweet,aggregate_tweets)
				else:
					recentInterest = 0
					continue



				#count number of follower Score start here:

				num_followers = int(d['num_followers'])
				empirical_based = num_followers*(cosine_sim*int(num_rt))

				recommendation_list_eb[user].append(empirical_based)

	top_15_eb = heapq.nlargest(15, recommendation_list_eb, key=recommendation_list_eb.get)

	return top_15_eb

evaluateSimilarityJSON(user,tweet