import os
import sys
import numpy as np
import getopt
import nltk.classify
from sklearn.svm import LinearSVC
import pickle
import io


if __name__ == "__main__":
    """
    Usage: python svmtrain.py -m <path/to/model/file> path/to/training/file
    """

    path = ""
    model = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hm:", ["model="])
    except getopt.GetoptError:
        print "Usage: python svmtrain.py -m <path/to/model/file> path/to/training/file"
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print "Usage: python svmtrain.py -m <path/to/model/file> path/to/training/file"
            sys.exit(0)
        elif opt in ("-m", "--model"):
            model = arg

    if len(args) > 0:
        path = args[0]
    else:
        print "Usage: python svmtrain.py -m <path/to/model/file> path/to/training/file"
        sys.exit(2)

    # Check training file is exists or not?
    if not os.path.exists(path):
        print "The training file \'%s\' is not exists. Try again!" % path
        sys.exit(1)
    elif not os.path.isfile(path):
        print "The training file \'%s\' is not a file. Try again!" % path
        sys.exit(1)

    # Load training data
    print "Loading training data..."
    traindata = np.load(path)

    # Make classifier from Scikit-learn with NLTK Classify interface
    cls = nltk.classify.SklearnClassifier(LinearSVC(verbose=1))

    # Training
    print "Training LinearSVC Model from the data \'%s\'" % path
    cls.train(traindata)

    # Saving model
    print "Saving model into file \'%s\'" % model
    with io.open(model, 'wb') as fmodel:
        pickle.dump(cls, fmodel)

    # Finished?
    print "DONE!!"
