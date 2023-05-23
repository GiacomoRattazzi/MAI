import csv
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
from tqdm import tqdm
def preprocess_tweet(tweet):
    tweet_words = []

    for word in tweet.split(' '):
        if word.startswith('@') and len(word) > 1:
            word = '@user'
        elif word.startswith('http'):
            word = "http"
        print(word)
        tweet_words.append(word)


    return " ".join(tweet_words)

# Load model and tokenizer
roberta = "cardiffnlp/twitter-roberta-base-sentiment"
model = AutoModelForSequenceClassification.from_pretrained(roberta)
tokenizer = AutoTokenizer.from_pretrained(roberta)

# List of CSV files
csv_files = [
    'tweets_oct20.csv',
    'tweets_nov20.csv',
    'tweets_dec20.csv',
    'tweets_jan21.csv',
    'tweets_feb21.csv',
]

# List to store the results for each file
results = []

for csv_file in csv_files:
    # Read the CSV file
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row

        tweet_data = [row for row in reader]

    # Calculate sentiment for each tweet
    sentiments = []
    for row in tqdm(tweet_data):
        content = row[3]  # Get the content of the tweet
        preprocessed_tweet = preprocess_tweet(content)
        encoded_tweet = tokenizer(preprocessed_tweet, return_tensors='pt')
        output = model(**encoded_tweet)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)

        sentiment = scores[2] - scores[0]  # Positive score - Negative score
        sentiments.append(sentiment)

    # Calculate the average sentiment
    average_sentiment = sum(sentiments) / len(sentiments)

    # Add the results to the list
    results.append({'file': csv_file, 'average_sentiment': average_sentiment})

# Save the results to a CSV file
with open('sentiment_results.csv', mode='w', encoding='utf-8') as f:
    fieldnames = ['file', 'average_sentiment']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for result in results:
        writer.writerow(result)

# Print the average sentiments for each month
for result in results:
    print(f"Average sentiment for {result['file']}: {result['average_sentiment']}")
