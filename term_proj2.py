import sys
import json
import wx
import operator
#Mark Pierce
#Uvic csc485C
#Oct 22, 2013

hashtags = dict()
users = dict()
text = ""

class TwitterPanel(wx.Panel):
	global hashtags
	global users
	global text
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
		self.quote = wx.StaticText(self, label="Enter a User or Hashtag", pos=(20, 30))
		
		# A multiline TextCtrl - This is here to show how the events work in this program, don't pay too much attention to it
		self.logger = wx.TextCtrl(self, pos=(20,120), size=(200,300), style=wx.TE_MULTILINE | wx.TE_READONLY)

		# A button
		self.button =wx.Button(self, label="Go", pos=(55, 80))
		self.Bind(wx.EVT_BUTTON, self.OnClick,self.button)
		

		# the edit control - one line version.
		self.lblname = wx.StaticText(self, label="Query:", pos=(20,60))
		self.editname = wx.TextCtrl(self, value="Enter a User or Hashtag", pos=(55, 59), size=(145,-1))
		self.Bind(wx.EVT_TEXT, self.EvtText, self.editname)
		self.Bind(wx.EVT_CHAR, self.EvtChar, self.editname)
		
		#self.Bind(wx.EVT_PAINT, self.OnPaint)
		
	
	def OnClick(self,event):
		global text
		#print 2
		#self.Bind(wx.EVT_PAINT, self.OnPaint)
		
		if text.startswith("#"):
			text = text.replace("#","")
			#print text
			if text in hashtags.keys():
				temp = hashtags[text].pop("hashtag_total_score")
				self.logger.AppendText(text + ", words used with this hashtag: \n")
				for y in hashtags[text]:
					self.logger.AppendText(y +" %d \n" % hashtags[text][y])
				self.logger.AppendText("Total score of "+ text +": %s \n" % temp)
			else:
				self.logger.AppendText("This hashtag has not been mentioned\n")
		else:
			if text in users.keys():
				temp = users[text].pop("user_total_score")
				self.logger.AppendText(text + ", words used with this user: \n")
				for y in users[text]:
					self.logger.AppendText(y + " %d \n" % users[text][y])
				self.logger.AppendText("Total score of "+ text +": %s \n" % temp)
			else:
				self.logger.AppendText("This user has not been mentioned.  Did you mean to search for a hashtag?  Remember to use the \"#\" symbol\n")
		
		
	def EvtText(self, event):
		global text
		text = event.GetString()
		#self.logger.AppendText('EvtText: %s\n' % event.GetString())
	def EvtChar(self, event):
		self.logger.AppendText('EvtChar: %d\n' % event.GetKeyCode())
		event.Skip()
	
def tofile(out_file, screen_name, id, tweet_name, tweet_hashtag, user_mention, place, location, tweet_text, coordinates, user_location, created_at):
	#print 'i made it here'
	out_file.write(screen_name+', '+tweet_name+', '+id+', '+created_at+', '+tweet_text+', '+location+', '+place+', '+user_location+', '+tweet_hashtag+', '+user_mention+'\n')
	
	
def hw():
    print 'Hello, world!'

def lines(fp):
    return str(len(fp.readlines()))

def main():
	sent_file = open(sys.argv[1])
	tweet_file = open(sys.argv[2])
	out_file = open('tweetsheet.txt', "w")
	scores = {}
	text = ""
	global hashtags
	global users
	
	count = 0
	place_count = 0
	location_count = 0
	user_loc_count = 0

	#out_file.write("")
	out_file.write("screen name, name, id, created_at, text, location, place, user location, hashtags used, users mentioned\n")
	
	for line in sent_file:
		term, score  = line.split("\t")  
		scores[term] = int(score)  
	#print scores
	for line in tweet_file:
		tweet = json.loads(line)
		screen_name = ''
		id = ''
		tweet_name = ''
		tweet_hashtag = ''
		user_mention = ''
		place = ''
		location = ''
		tweet_text = ''
		coordinates = ''
		user_location = ''
		created_at = ''
		
		if 'entities' in tweet:
			#print tweet['entities']
			if 'hashtags' in tweet['entities']:
				for value in tweet['entities']['hashtags']:
					#print value
					#print type(value)
					if 'text' in value:
						name = value['text']
						tweet_hashtag = name.encode('ascii', 'ignore')
						if 'text' in tweet:
							temp = tweet['text'].encode('ascii', 'ignore')
							for word in temp.split(' '):
								if word in scores.keys():
									#print type(name)
									hashtag = name.encode('ascii', 'ignore')
									if temp2 in hashtags.keys():
										if word in hashtags[temp2].keys():
											hashtags[temp2][word] = hashtags[temp2][word] + 1
										else:
											hashtags[temp2][word] = 1
									else:
										hashtags[temp2] = {word: 1}
			if 'user_mentions' in tweet['entities']:
					#print type(tweet['entities']['user_mentions'])
					for value in tweet['entities']['user_mentions']:
						#print type(value)
						#print value
						if 'screen_name' in value:
							name = value['screen_name']
							user_mention = name.encode('ascii', 'ignore')
							if 'text' in tweet:
								temp = tweet['text'].encode('ascii', 'ignore')
								for word in temp.split(' '):
									if word in scores.keys():
										#print type(name)
										temp2 = name.encode('ascii', 'ignore')
										if temp2 in users.keys():
											if word in users[temp2].keys():
												users[temp2][word] = users[temp2][word] + 1
											else:
												users[temp2][word] = 1
										else:
											users[temp2] = {word: 1}
		if 'created_at' in tweet:
			created_at = tweet['created_at'].encode('ascii','ignore')
		if 'text' in tweet:
			tweet_text = tweet['text'].encode('ascii','ignore')
			#print tweet_text
			#print type(tweet_text)
			tweet_text = tweet_text.replace('\n', ' ')
		if 'id' in tweet:
			id = str(tweet['id'])
		
		if 'place' in tweet:
			if tweet['place'] != None:
				#print tweet['place']
				place = str(tweet['place']).encode('ascii','ignore')
				place_count = place_count+1
		if 'coordinates' in tweet:
			if tweet['coordinates'] != None:
				#print tweet['coordinates']
				coodinates = str(tweet['coordinates']).encode('ascii','ignore')
				location_count = location_count+1
		if 'user' in tweet:
			if 'location' in tweet['user']:
				if tweet['user']['location'] != None:
					user_location = tweet['user']['location'].encode('ascii', 'ignore')
					#print tweet['user']['location'].encode('ascii', 'ignore')
					user_loc_count = user_loc_count+1
			if 'name' in tweet['user']:
				tweet_name = tweet['user']['name'].encode('ascii','ignore')
			if 'screen_name' in tweet['user']:
				screen_name = tweet['user']['screen_name'].encode('ascii','ignore')
		tofile(out_file, screen_name, id, tweet_name, tweet_hashtag, user_mention, place, location, tweet_text, coordinates, user_location, created_at)
		
	for x in hashtags:
		for y in hashtags[x]:
			count  = count + hashtags[x][y]*scores[y]
		hashtags[x]['hashtag_total_score'] = count
		count = 0
	#print 'hashtags', hashtags, '\n'
	for x in users:
		for y in users[x]:
			count  = count + users[x][y]*scores[y]
		users[x]['user_total_score'] = count
		count = 0
	#print users
	#print hashtags
	#max_variable = max(hashtags.iteritems(), key=operator.itemgetter(1))[0]
	#print max_variable, hashtags[max_variable]['hashtag_total_score']
	print 
	print 'place:', place_count
	print 'location:', location_count
	print 'user location:', user_loc_count
	out_file.close()
	#app = wx.App(False)
	#frame = wx.Frame(None)
	#panel = TwitterPanel(frame)
	#frame.Show()
	#app.MainLoop()
	
	
if __name__ == '__main__':
    main()
