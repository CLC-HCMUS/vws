import sys
import numpy as np
import getopt
import os
import pickle
#from nltk import MaxentClassifier
from nltk import classify

if __name__ == "__main__":
    """
    Usage: python test.py -m <path/to/model/file> path/to/test/file
    """

    path = ""
    model = ""

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hm:", ["model="])
    except getopt.GetoptError:
        print "Usage: python test.py -m <path/to/model/file> path/to/test/file"
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print "Usage: python test.py -m <path/to/model/file> path/to/test/file"
            sys.exit(0)
        elif opt in ("-m", "--model"):
            model = arg

    # Check model file is exists or not?
    if not os.path.exists(model):
        print "The model file \'%s\' is not exists. Try again!" % model
        sys.exit(2)
    elif not os.path.isfile(model):
        print "The model file \'%s\' is not a file. Try again!" % model
        sys.exit(2)

    if len(args) > 0:
        path = args[0]
    else:
        print "Usage: python test.py -m <path/to/model/file> path/to/test/file"
        sys.exit(2)

    # Check test file is exists or not?
    if not os.path.exists(path):
        print "The test file \'%s\' is not exists. Try again!" % path
        sys.exit(2)
    elif not os.path.isfile(path):
        print "The test file \'%s\' is not a file. Try again!" % path
        sys.exit(2)

    # Load test data
    print "Loading test data..."
    testset = np.load(path)

    # Load model
    print "Loading model..."
    fmodel = open(model, 'rb')
    maxent = pickle.load(fmodel)
    fmodel.close()

    # Run test
    print "Testing..."
    accuracy = classify.accuracy(maxent, testset)
    print "Accuracy: %.4f" % accuracy

    # Finished?
    print "DONE!!"
