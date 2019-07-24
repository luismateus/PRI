import sys, csv, string
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from sklearn import metrics

# Classifiers
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn import svm


csv.field_size_limit(sys.maxsize)
def from_csv():
    data = pd.read_csv("en_docs_clean.csv", sep=',')
    return data

def tokenizer(data):
    count_vect = CountVectorizer()
    x_train_counts = count_vect.fit_transform(data["text"])
    x_train_counts.shape
    return x_train_counts, count_vect


def tfidf_transformer(x_train_counts):
    tf = TfidfTransformer()
    x_train_tfidf = tf.fit_transform(x_train_counts)
    x_train_tfidf.shape
    return tf, x_train_tfidf

def train_classifier(clf,x_train_tfidf, data):
    clf.fit(x_train_tfidf , data["party"])
    return clf

def predict_party(clf, count_vect, tf):
    inputText = sys.argv[1:]
    text = ' '.join(inputText)
    if(text == ''):
       predicted = 0
       return predicted
    query = format_text(text)
    x_new_counts = count_vect.transform([query])
    x_new_tfidf = tf.transform(x_new_counts)
    predicted = clf.predict(x_new_tfidf)
    return predicted

def format_text(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text.lower())
    filtered_words = [w for w in word_tokens if w not in stop_words and w not in string.punctuation] #n
    new_query = ' '.join(filtered_words)
    return new_query


def predict_list(clf, count_vect, x_test, tf):
   x_new_counts = count_vect.transform(x_test["text"])
   x_new_tdidf = tf.transform(x_new_counts)
   predicted = clf.predict(x_new_tdidf)
   return predicted

#recall, precision and F1

# def calc_precision(predicted, correct): #average value?
#    return metrics.precision_score(correct, predicted, average=None)

# def calc_recall(predicted, correct):
#    return metrics.recall_score(correct, predicted, average=None)

# def calc_F1(predicted, correct):
#    return metrics.f1_score(correct, predicted, average=None)

def confusion_matrix(predicted, correct):
   l = ["Conservative Party", "Democratic Unionist Party", "Green Party of England and Wales", "Labour Party", "Liberal Democrats", "Scottish National Party", "Social Democratic and Labour Party", "The Party of Wales", "Ulster Unionist Party","United Kingdom Independence Party","We Ourselves"]
   return metrics.confusion_matrix(correct, predicted, labels = l)

data = from_csv()

def predict_from_text():
   x_train_counts, count_vect = tokenizer(data)
   tf, x_train_tfidf = tfidf_transformer(x_train_counts)
   
   #clf = SGDClassifier()
   #clf = MultinomialNB()
   clf = svm.LinearSVC()
   
   clf = train_classifier(clf, x_train_tfidf, data)
   predicted = predict_party(clf,count_vect, tf)
   if(predicted==0):
      print("No input text given")
   else:
      print("\nThe political party most likely to have produced the text is: " + predicted[0] + '\n')

def predict_from_test():
   x_train, x_test = train_test_split(data, test_size=0.2)
   x_train_counts, count_vect = tokenizer(x_train)
   tf, x_train_tfidf = tfidf_transformer(x_train_counts)
   
   #clf = SGDClassifier()
   #clf = MultinomialNB()
   clf = svm.LinearSVC()
   

   clf = train_classifier(clf ,x_train_tfidf, x_train)
   predicted = predict_list(clf, count_vect, x_test, tf)

   #print("Accuracy: "+ str(np.mean(predicted == x_test["party"])))

   c_matrix = confusion_matrix(predicted,x_test["party"])
   print(metrics.classification_report(x_test["party"], predicted))
   print("confusion matrix:\n",c_matrix)
   
predict_from_text()
predict_from_test()