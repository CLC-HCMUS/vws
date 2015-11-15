import sys
import numpy as np
import getopt
import os
from nltk import MaxentClassifier
import pickle
import io

if __name__ == '__main__':
    """
    Usage: python train.py -m <path/to/model/file> path/to/training/data
    """

    path = ""
    model = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hm:", ["model="])
    except getopt.GetoptError:
        print "Usage: python train.py -m <path/to/model/file> path/to/training/data"
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print "Usage: python train.py -m <path/to/model/file> path/to/training/data"
            sys.exit(0)
        elif opt in ("-m", "--model"):
            model = arg

    if model == "":
        print "Usage: python train.py -m <path/to/model/file> path/to/training/data"
        sys.exit(2)

    if len(args) > 0:
        path = args[0]
    else:
        print "Usage: python train.py -m <path/to/model/file> path/to/training/data"
        sys.exit(2)

    # Check the path is exists or not?
    if not os.path.exists(path):
        print "The path \'%s\' is not exist. Try again!" % path
        sys.exit(2)
    elif not os.path.isfile(path):
        print "The path \'%s\' is not a file. Try again!" % path
        sys.exit(2)

    # Load dataset
    print "Loading training data..."
    dataset = np.load(path)

    # Training processing
    print "Training Maximum Entropy Model from the dataset \'%s\'" % path
    maxent = MaxentClassifier.train(dataset, max_iter=10)


    # Save model
    print "Saving model into file %s" % model
    with io.open(model, 'wb') as fmodel:
        pickle.dump(maxent, fmodel)

    # Finished?
    print "DONE!!"
