# MAI

# Repository structure 
```

│
├── Tweets
│   └── Code
│       └── senTweets.py
│       └── tweetScraper.py
│   └── Data
│       └── tweets_dec20.csv
│       └── tweets_feb21.csv
│       └── tweets_jan21.csv
│       └── tweets_nov20.csv
│       └── tweets_oct20.csv
│   └── Visualizations
│  
├── Articles
│   └── Code
│       └── articles.py
│   └── Data
│       └── articles_results.csv
│       └── articles_text.csv
│   └── Visualizations
│ 
│── README.md
```

# Tweets

This section contains Python scripts for scraping and analyzing tweets. The scripts are:
* tweetScraper.py: This script is used to scrape tweets from Twitter using Selenium. The code for this script was adapted from another project, [TwitterWebScraper](https://github.com/wilfredNJH/TwitterWebScraper-) repository on GitHub, wilfredNJH.
* senTweets.py: This script is used for sentiment analysis of tweets. It uses the transformers library to load a pre-trained model 'cardiffnlp/twitter-roberta-base-sentiment' for sentiment analysis. The code for this script was adapted from another project, [tw-sentiment.py](https://github.com/mehranshakarami/AI_Spectrum/blob/main/2022/Sentiment_Analysis/tw-sentiment.py) by mehranshakarami.

# Articles

* articles.py 
