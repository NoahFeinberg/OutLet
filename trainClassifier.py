from textblob.classifiers import NaiveBayesClassifier
import cPickle as pickle

with open('train_500.csv', 'r') as fp:
    print "Started Training"
    cl = NaiveBayesClassifier(fp, format="csv")
    trained_classifier_file = open('trained_classifier_500.pickle', 'wb')
    pickle.dump(cl, trained_classifier_file)
    print "Stop Training"

print cl.classify('mr. speaker , will the gentleman yield ?')
