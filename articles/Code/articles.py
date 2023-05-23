import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re
from collections import Counter

# Read the CSV file
df = pd.read_csv("articles_results.csv")

# Compute the average sentiment for each month
monthly_sentiment = df.groupby("Date")["Sentiment"].mean()

# Specify the order of months
month_order = ["Nov-20", "Dec-20", "Jan-21", "Nov-21", "Dec-21", "Jan-22"]

# Reindex the monthly_sentiment DataFrame with the specified order
monthly_sentiment = monthly_sentiment.reindex(month_order)

# Function to plot average sentiment
def plot_sentiment(df, start_month, end_month, y_range=None, filename="average_sentiment.pdf"):
    plt.figure(figsize=(10, 5))
    plt.plot(df[start_month:end_month].index, df[start_month:end_month].values)
    plt.xlabel("Month")
    plt.ylabel("Average Sentiment")
    plt.title(f"Average Sentiment from {start_month} to {end_month}")

    # Add the exact value on each point
    for x, y in zip(df[start_month:end_month].index, df[start_month:end_month].values):
        plt.text(x, y, f"{y:.4f}", fontsize=8, ha='left', va='bottom')

    if y_range is not None:
        plt.ylim(y_range)
    plt.savefig(filename)

# Plot the chronological graph of the average sentiments
plot_sentiment(monthly_sentiment, "Nov-20", "Jan-21", filename="average_sentiment_20-21.pdf")
plot_sentiment(monthly_sentiment, "Nov-20", "Jan-21", y_range=(-1, 1), filename="average_sentiment_20-21_fixed_y.pdf")
plot_sentiment(monthly_sentiment, "Nov-21", "Jan-22", filename="average_sentiment_21-22.pdf")
plot_sentiment(monthly_sentiment, "Nov-21", "Jan-22", y_range=(-1, 1), filename="average_sentiment_21-22_fixed_y.pdf")

# Function to extract words from MainSubject
def extract_words(main_subject):
    return re.findall(r'(\w+)\s+\d+\.\d+', main_subject)

# Create wordcloud for each month
for month, data in df.groupby("Date"):
    words = " ".join(data["MainSubject"].apply(extract_words).explode())
    wordcloud = WordCloud(width=800, height=800, background_color="white").generate(words)
    plt.figure(figsize=(8, 8))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(f"wordcloud_{month}.pdf")

# Create bar charts for top 5 words for each month
for month, data in df.groupby("Date"):
    all_words = data["MainSubject"].apply(extract_words).explode()
    word_count = Counter(all_words).most_common(5)

    words, counts = zip(*word_count)
    plt.figure(figsize=(10, 5))
    plt.bar(words, counts)
    plt.xlabel("Words")
    plt.ylabel("Frequency")
    plt.title(f"Top 5 Words for {month}")
    plt.savefig(f"top5words_{month}.pdf")
