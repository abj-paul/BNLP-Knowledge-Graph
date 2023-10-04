import joblib
import gensim
import re
from gensim.utils import simple_preprocess
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import gensim.corpora as corpora# Create Dictionary
from pprint import pprint# number of topics

stop_words = stopwords.words('english')
stop_words.extend(['from', 'subject', 're', 'edu', 'use'])

parsed_results = joblib.load("parsed_papers.joblib")

def normalize(text):
    text = re.sub('[,\.!?]', '', text)
    text = text.lower() 
    return text

def sentence_to_words(sentence):
    return gensim.utils.simple_preprocess(str(sentence), deacc=True)

def remove_stopwords(word_list):
    words = []
    for word in word_list:
        if word not in stop_words:
            words.append(word)
    return words

# Generating Bag of Words
normalized_text = normalize(parsed_results[0]["abstract"])
words = list(sentence_to_words(normalized_text))
words = remove_stopwords(words)

# Encoding words to numbers
id2word = corpora.Dictionary([words,words])# Create Corpus
corpus = id2word.doc2bow(words)

# LDA
num_topics = 10# Build LDA model
lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                       id2word=id2word,
                                       num_topics=num_topics)# Print the Keyword in the 10 topics
pprint(lda_model.print_topics())
doc_lda = lda_model[corpus]

