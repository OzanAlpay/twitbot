#!/usr/bin/env python2.7
import tweepy
from peewee import *
import time
#Copied from Twitter Application
consumer_key =  'ADD YOUR CONSUMER KEY HERE'
consumer_secret = 'ADD YOUR CONSUMER SECRET HERE'
access_token = 'ADD YOUR ACCESS TOKEN'
access_token_secret = 'ADD YOUR ACESS TOKEN SECRET'
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)
me = api.me()
#End of Twitter API Auth
#Start of connect to MySql Database with peewee, and create table Complain
db = MySQLDatabase('Complains', user='GiveYourUserName', passwd='GiveYourPasswd')

db.connect()
db.set_autocommit(True)
class Complain(Model):
	user_screen_name=TextField()
	received_time=DateTimeField()
	text_message=TextField()
	class Meta:
		database = db
create_tables=db.get_tables()
if not create_tables:
	Complain.create_table()
#End of peewee part
#Get read last mention ( to avoid read tweets again and again)
f = open("lastid.txt","r")
since=f.read()
f.close()
#End of read last mention
while True:
	mentions = api.mentions_timeline(since_id=since)
	print "Working...."
	for mention in mentions:
		print "ID " , mention.id
		newsince=mention.id
		print newsince
		name=mention.user.screen_name
		text=mention.text
		receive_time=mention.created_at
		tempcomplain=Complain(user_screen_name=name, received_time=receive_time, text_message=text)
		tempcomplain.save()
		print name,text,receive_time
		#If you want to send another message to sender , change the " your message received part" and make it whatever you want
		api.update_status("@"+name+" your message received")
		f = open("lastid.txt","w")
		f.write(str(newsince))
		f.close()
	#If you delete time.sleep part the program use the twitterAPI so much , and twitter will ban your account.
	print "Sleeping"
	time.sleep(60)
	
	
