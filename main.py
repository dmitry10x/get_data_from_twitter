#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import tweepy
from config import *
from textblob import TextBlob

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def find_tweets(key_word, tweets_quantity_to_get, user_to_avoid, max_id=''):
    tweets_list = []
    tweets_quantity = 0
    counter = 0

    public_tweets = api.search(str(key_word), count=99)
    while tweets_quantity < tweets_quantity_to_get:

        length = len(public_tweets)
        for tweet in public_tweets:
            counter += 1

            if tweet._json['user']['name'] != str(user_to_avoid):
                tweets_list.append({'message_id': tweet._json['id'], 'message_text': tweet.text})
                tweets_quantity += 1

            if counter == length:
                max_id = tweet._json['id']
                counter = 0
                public_tweets = api.search(str(key_word), count=99, max_id=max_id)
                break

    return tweets_list



def make_csv(csv_name, tweets_list):
    csv_name = '{}.csv'.format(str(csv_name))
    with open(csv_name, 'w', encoding='utf-8') as f:
        f = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in tweets_list:
            f.writerow([str(i['message_id']), str(i['message_text'])])


# tweets = find_tweets('ozon.ru', 1000, 'OZON')
# print(tweets)
# make_csv('new_100', tweets)

