import feedparser
import json
from datetime import datetime, timedelta
import dateparser
import nltk
import os
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer

def get_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(text)["compound"] >= 0

def get_last_post_timestamp() -> int:

    current_timestamp = int(datetime.now().timestamp())
    last_post_update = current_timestamp

    current_dir = os.path.dirname(os.path.realpath(__file__)) + "/data.json"

    # read timestamp from file
    try:
        with open(current_dir, "r") as f:
            last_post_update = int(json.loads(f.read())["last_post"])
    except Exception as e:
        pass

    # write timestamp to json file
    with open(current_dir, "w") as f:
        f.write(json.dumps({"last_post": current_timestamp}))

    return last_post_update

def get_news(rss_feed):
    last_post_timestamp = get_last_post_timestamp()
    #yesterday = datetime.today() - timedelta(days=1)
    NewsFeed = feedparser.parse(rss_feed)
    news_dict = []
    for entry in NewsFeed.entries:
        if int(dateparser.parse(entry.published).timestamp()) >= last_post_timestamp:
            news_dict.append(
                {
                    'title': entry.title,
                    'summary': entry.summary,
                    'link': entry.link,
                    'sentiment': get_sentiment(entry.summary)
                }
            )
    return news_dict

def get_all_news(infile):
    all_news = []
    with open(infile, 'r') as fin:
        for rss in fin.readlines():
            all_news.extend(get_news(rss))
    fin.close()
    return all_news