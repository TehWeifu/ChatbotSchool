# Load all the nlu_fallback from mongo and create a topic model to detect the most common topics.

import os

import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pymongo import MongoClient
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

# import pyLDAvis

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
TOPIC_COUNT = 3
RANDOM_STATE = 2055
STOP_WORDS = set(stopwords.words('spanish'))
nlp = spacy.load("es_core_news_lg")


def remove_stop_words(sentence):
    word_tokens = word_tokenize(sentence)
    filtered_sentence = [word for word in word_tokens if word.lower() not in STOP_WORDS]
    return ' '.join(filtered_sentence)


def lemmatize_text(text):
    doc = nlp(text)
    lemmatized_text = ' '.join([token.lemma_ for token in doc])
    return lemmatized_text


def create_lda_model(data, topic_number):
    model = LatentDirichletAllocation(n_components=topic_number, max_iter=5, random_state=RANDOM_STATE)
    model.fit(data)

    doc_topic_distribution = model.transform(data)
    topic_word_distribution = model.components_

    return model, doc_topic_distribution, topic_word_distribution


def print_lda_topics(topic_word_distribution, feature_names, top_word_number=5):
    print("\nDistribución de palabras para cada tópico:")
    for i, topic_words in enumerate(topic_word_distribution):
        top_words_indices = topic_words.argsort()[-top_word_number:][::-1]
        top_words = [feature_names[index] for index in top_words_indices]
        print(f"Tópico {i + 1}: {top_words}")


# def display_lda_topics(model, X, vectorizer):
#     panel = pyLDAvis.lda_model.prepare(model, X, vectorizer, mds='tsne')
#     return pyLDAvis.display(panel)


# Connect to MongoDB
uri = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@mycluster.xkgnpk7.mongodb.net/?retryWrites=true&w=majority&appName=MyCluster"
client = MongoClient(uri)
db = client.rasa
conversations = db.conversations

# Fetch texts detected as nlu_fallback
pipeline = [
    {"$unwind": "$events"},
    {"$match": {"events.event": "user", "events.parse_data.intent.name": "nlu_fallback"}},
    {"$project": {"text": "$events.text"}},
]
results = conversations.aggregate(pipeline)
corpus = [result["text"] for result in results]
corpus = [lemmatize_text(text) for text in corpus]
corpus = [remove_stop_words(text) for text in corpus]
# print(corpus)

# Tokenize the corpus, lemmatize and remove stop words
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(corpus)
terms_dictionary = vectorizer.get_feature_names_out()

# Create LDA model and print topics
lda_model, lda_doc_topic_distribution, lda_topic_word_distribution = create_lda_model(X, TOPIC_COUNT)
print_lda_topics(lda_topic_word_distribution, terms_dictionary)
# display_lda_topics(lda_model, X, vectorizer)
