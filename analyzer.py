from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import cPickle as pickle
import time
# from nltk import grammar
# from stat_parser import Parser


# query = "Starbucks was one of those early to criticize President Trump for putting a temporary hold on immigration from a list of seven terror-torn countries flagged by the Obama administration. In response, the coffee house giant pledged to hire 10,000 Muslim refugees over five years in protest against Drumpfs order."

# parser = Parser()

# print parser.parse(query)

cl = pickle.load(open('trained_classifier.pickle', 'r'))
query = raw_input("Article: ")

query = query.decode('ascii', errors="ignore")
output = TextBlob(query, classifier=cl, analyzer=NaiveBayesAnalyzer())

print output.sentiment

