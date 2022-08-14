import tweepy
from scraper import get_all_news
from PIL import Image
from datetime import datetime
import configparser

config_obj = configparser.ConfigParser()
config_obj.read("config.ini")
creds = config_obj["creds"]
color = config_obj["color"]

auth = tweepy.OAuthHandler(creds["CONSUMER_KEY"], creds["CONSUMER_SECRET"])
auth.set_access_token(creds["ACCESS_TOKEN"], creds["ACCESS_TOKEN_SECRET"])

api = tweepy.API(auth)
to_tweet = get_all_news("rss_feeds.txt")

today = color["TODAYS_COLOR"]
color_counter = 0
sent_dict = {True: "positive", False: "negative"}
for tweet in to_tweet:
    api.update_status(tweet.get("title") + "\nSentiment: " + sent_dict.get(tweet.get("sentiment")) + "\n" + tweet.get("link"))
    if tweet.get("sentiment"):
        color_counter += 1
    else:
        color_counter -= 1

todays_date = datetime.now().strftime("%d%m%y")
today = hex(int(today, 16) + color_counter*65793)[2:]
color["TODAYS_COLOR"] = today
with open("config.ini", "w") as edit:
    config_obj.write(edit)
im = Image.new("RGB", (400,400), "#"+today)
im.save(todays_date + ".png")
api.update_profile_image(todays_date + ".png")