import re 
from textblob import TextBlob

#Function used to clean tweets for sentiment analysis for the Twitcalls() in BoxSentimentPage() and
# NoBoxSentimentPage(). 
def clean_tweet(tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", str(tweet)).split()) 

#This comment applies a sentiment value from Textblob to a tweet given from the Twitcalls() in BoxSentimentPage() and NoBoxSentimentPage(). 
def get_tweet_sentiment(tweet): 
        ''' 
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        '''
	
        analysis = TextBlob(clean_tweet(tweet)) 
       
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'

#Character parser to turn the characters of numbers into their numeric equivalent  for the Twitcalls() in BoxSentimentPage() and NoBoxSentimentPage()
def charparser(ch):
	if ch == '1':
		return 1
	elif ch == '2':
		return 2
	elif ch == '3':
		return 3
	elif ch == '4':
		return 4
	elif ch == '5':
		return 5
	elif ch == '6':
		return 6
	elif ch == '7':
		return 7
	elif ch == '8':
		return 8
	elif ch == '9':
		return 9
	elif ch == '0':
		return 0
	else:
		return -1
	
#Turn a string value for the total number of retweets and favorites of a tweet into a numerical value  for the Twitcalls() in BoxSentimentPage() and NoBoxSentimentPage()
def stringparser(st):
	rig = 'sfdsfdsf'
	if type(st) == type(rig):

		if st.find( 'K' ) != -1:
			fin = 0		
			leng= len(st)
			itera = 0
			hold = -1
			while itera < (leng-1):
				#fin = fin * 10
				temp = charparser(st[itera])
				if temp == (-1):
					hold = 1
				else:
					fin = fin * 10
					fin = fin + temp
					if hold == 1:
						fin = fin * 100
				itera = itera + 1
			return fin				
				
			
			
		
		
		else:
			return st
	else:
		return st
