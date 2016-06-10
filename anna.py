from __future__ import print_function
import ConfigParser
import json
import eliza
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
import textwrap
from Adafruit_Thermal import *
#printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)

config = ConfigParser.ConfigParser()
config.read('.twitter')

consumer_key = config.get('apikey', 'key')
consumer_secret = config.get('apikey', 'secret')
access_token = config.get('token', 'token')
access_token_secret = config.get('token', 'secret')
stream_rule = config.get('app', 'rule')
account_screen_name = config.get('app', 'account_screen_name').lower() 
account_user_id = config.get('app', 'account_user_id')

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitterApi = API(auth)

therapist = eliza.eliza();

class ReplyToTweet(StreamListener):

    def on_data(self, data):
	print(1)
        print(data)
	print(2)
        tweet = json.loads(data.strip())
        
        retweeted = tweet.get('retweeted')
        from_self = tweet.get('user',{}).get('id_str','') == account_user_id

        if retweeted is not None and not retweeted and not from_self:

            tweetId = tweet.get('id_str')
            screenName = tweet.get('user',{}).get('screen_name')
            tweetText = tweet.get('text')
	    print(4)
            tweetText = tweetText.encode('UTF-8')
            print(tweetText)
            chatResponse = therapist.respond(tweetText)
            print(chatResponse)
            print(5)
            replyText = '@' + screenName + ' ' + chatResponse
            print(6)
           
            #check if repsonse is over 140 char
            if len(replyText) > 130:
                replyText = replyText[0:127] + '...'

            wrappedTweet = textwrap.fill(tweetText, 32)
            wrappedReply = textwrap.fill(replyText, 32)
            printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)

            printer.println('Tweet ID: ' + tweetId)
            printer.println('From: ' + screenName)
            printer.println('Tweet Text:')
            printer.println(wrappedTweet)
            printer.println('Reply Text:')
            printer.println(wrappedReply)
            printer.feed(3)


            # If rate limited, the status posts should be queued up and sent on an interval
            twitterApi.update_status(status=replyText, in_reply_to_status_id=tweetId)
            print(7)
    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    streamListener = ReplyToTweet()
    twitterStream = Stream(auth, streamListener)
    twitterStream.userstream(_with='user')
