##ALWAYS RUN 
##export GOOGLE_APPLICATION_CREDENTIALS="/Users/hakang/Documents/tweepy/angular-spider-343319-cbf0fc9b4970.json" 
##in the terminal

import pandas as pd
import numpy as np
import tweepy
import json
import html
from random import randrange


def translate_text(target, text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    import six
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)

    #print(u"Text: {}".format(result["input"]))
    #print(u"Translation: {}".format(result["translatedText"]))
    #print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))
    return(result["translatedText"])

auth = tweepy.OAuth2AppHandler(
    "9GA3TLN7tirIcENV4thp4QNl5", "XBirb06QeDJoQyx4M1eqFRUzHRu2Ul7IWjbmjKsKNzZMYWn4Ep"
)
api = tweepy.API(auth)

auth = tweepy.OAuth1UserHandler(
   "9GA3TLN7tirIcENV4thp4QNl5", "XBirb06QeDJoQyx4M1eqFRUzHRu2Ul7IWjbmjKsKNzZMYWn4Ep",
   "1500305139801882626-NA3XOoKHDQIgtV0rM5eSVzeCUsZ2mN", "nLJK9wCuMauOFjB0FgaEqV4aiEhlBPzcqGAih2hX5mI6I"
)
api = tweepy.API(auth)

list_users=["18949452","621523","19546277","253167239","624413", "69620713","1652541", "1333467482","807095","16449615","108710103","14594760", "935785877841645568", "14131762", "108740292", "137253079", "34713362","5988062", "928759224599040001", "2834511"]

# investingcom: "988955288" cnbc:"20402945"


class StreamListener(tweepy.Stream): 
    def on_status(self, status):
        if (('retweeted_status' not in status._json) and ('RT @' not in status._json) and (not bool(status._json.get('in_reply_to_status_id')))):
            #print(status._json)
            #print(status._json['created_at'])
            #print(status._json['user']['name'])
            if 'extended_tweet' in status._json:
                tr= translate_text('tr',status._json['extended_tweet']['full_text'])
            else:
                tr= translate_text('tr',status._json['text'])
            if ("@" not in status._json['text']) and ("LIVE" not in status._json['text']):
            	try:
            	    i=np.random.randint(22)
            	    if (i%3==2):
            	        api.update_status(status._json['user']['name']+": "+html.unescape(tr))
            	    print(i, status._json['user']['name']+": "+html.unescape(tr))
            	    print('\n')
            	except:
            	    print("LONG TWEET:")
            	    print(status._json['user']['name']+": "+html.unescape(tr))
            	    print('\n')
            #with open('tweet_json.txt', 'a') as file:
            #    file.write(json.dumps(status._json, indent=4))
            #finance_dicts.append(status._json)
        #print('\n')
    def on_error(self, status_code):
        if status_code == 420:
            return False
        
stream_listener = StreamListener("9GA3TLN7tirIcENV4thp4QNl5", "XBirb06QeDJoQyx4M1eqFRUzHRu2Ul7IWjbmjKsKNzZMYWn4Ep",
   "1500305139801882626-NA3XOoKHDQIgtV0rM5eSVzeCUsZ2mN", "nLJK9wCuMauOFjB0FgaEqV4aiEhlBPzcqGAih2hX5mI6I")

stream_listener.filter(follow=list_users)

