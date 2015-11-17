import os
import sys
import numpy as np
import pycrfsuite
from nltk.metrics import scores
from nltk.metrics import ConfusionMatrix
import getopt

if __name__ == '__main__':
    """
    Usage: python crftest.py -m <path/to/model/file> path/to/testing/file
    """

    path = ""
    model = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hm:", ["model="])
    except getopt.GetoptError:
        print "Usage: python crftest.py -m <path/to/model/file> path/to/testing/file"
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print "Usage: python crftest.py -m <path/to/model/file> path/to/testing/file"
            sys.exit(0)
        elif opt in ("-m", "--model"):
            model = arg

    if len(args) > 0:
        path = args[0]
    else:
        print "Usage: python crftest.py -m <path/to/model/file> path/to/testing/file"
        sys.exit(2)

    # Check the model file exists or not?
    if not os.path.exists(model):
        print "The model file \'%s\' does not exists. Try again!" % model
        sys.exit(1)
    elif not os.path.isfile(model):
        print "The model file \'%s\' is not a file. Try again!" % model
        sys.exit(1)

    # Check the testing file exists or not?
    if not os.path.exists(path):
        print "The testing file \'%s\' does not exists. Try again!" % path
        sys.exit(1)
    elif not os.path.isfile(path):
        print "The testing file \'%s\' is not a file. Try again!" % path
        sys.exit(1)

    # Loading testing file
    print "Loading the testing file ..."
    testset = np.load(path)

    # Convert testing set into CRF Feature Format
    featset = pycrfsuite.ItemSequence(testset[:, 0])
    ref = [str(label) for label in testset[:, 1]]

    # Loading the model
    print "Loading the CRF model..."
    tagger = pycrfsuite.Tagger()
    tagger.open(model)

    # Testing progress
    #sys.stdout.write("Testing: ")
    #sys.stdout.flush()
    #pred = []
    #idx = 0
    #for i in featset.items():
    #    idx += 1
    #    if idx % 1000 == 0:
    #        sys.stdout.write('.')
    #        sys.stdout.flush()
    #    pred.append(str(tagger.tag(i)))
    print "Testing..."
    pred = tagger.tag(featset)
    tagger.close()
    pred = [str(p) for p in pred]

    # Show result
    accuracy = scores.accuracy(ref, pred)
    print "\nAccuracy: %.4f" % accuracy
    cm = ConfusionMatrix(ref, pred)
    print "Confusion Matrix:"
    print (cm.pretty_format(sort_by_count = True, show_percents = True, truncate = 9))

    # Finished?
    print "DONE!!"
