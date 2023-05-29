import pandas as pd
from textblob import TextBlob
from gensim import corpora, models
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer
import nltk
import chardet
from nltk.corpus import stopwords

nltk.download('wordnet')

def lemmatize(text):
    return WordNetLemmatizer().lemmatize(text, pos='v')

def preprocess(text):
    nltk_stopwords = set(stopwords.words('english'))
    nltk_stopwords.add('say')
    print(nltk_stopwords)
    text = str(text)
    result = []
    for token in simple_preprocess(text):
        if token not in nltk_stopwords and len(token) > 3:
            result.append(lemmatize(token))
    return result


def get_main_subject(text, num_topics=3, passes=5):
    preprocessed_text = preprocess(text)
    if not preprocessed_text:  # Check if the preprocessed text is empty
        return 'Unknown'
    dictionary = corpora.Dictionary([preprocessed_text])
    corpus = [dictionary.doc2bow(preprocessed_text)]
    lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=passes)
    main_topic = sorted(lda_model.get_document_topics(corpus[0]), key=lambda x: -x[1])[0][0]
    topic_terms = lda_model.show_topic(main_topic)

    # Filter out 'say' from the topic words
    filtered_topic_terms = [(word, prob) for word, prob in topic_terms if word != 'say']

    # Create the topic string with probabilities, excluding 'say'
    topic_string = ', '.join([f'{word} {prob:.4f}' for word, prob in filtered_topic_terms])
    return topic_string


# Detect the encoding of the CSV file
csv_file = 'articles_text.csv'
with open(csv_file, 'rb') as file:
    result = chardet.detect(file.read())


# Load the CSV file with the detected encoding
df = pd.read_csv(csv_file, encoding=result['encoding'])

# Perform sentiment analysis
df['Sentiment'] = df['TEXT'].apply(lambda text: TextBlob(str(text)).sentiment.polarity)

# Get the main subject using topic modeling
df['MainSubject'] = df['TEXT'].apply(get_main_subject)

# Save the result to a new CSV file
df.to_csv('articles_results.csv', index=False)
