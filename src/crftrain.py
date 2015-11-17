import os
import sys
import getopt
import numpy as np
import pycrfsuite

if __name__ == '__main__':
    """
    Usage: python crftrain.py -m <path/to/model/file> path/to/training/file
    """

    path = ""
    model = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hm:", ["model="])
    except getopt.GetoptError:
        print "Usage: python crftrain.py -m <path/to/model/file> path/to/training/file"
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print "Usage: python crftrain.py -m <path/to/model/file> path/to/training/file"
            sys.exit(0)
        elif opt in ("-m", "--model"):
            model = arg

    if len(args) > 0:
        path = args[0]
    else:
        print "Usage: python crftrain.py -m <path/to/model/file> path/to/training/file"
        sys.exit(2)

    # Check the training file exists or not?
    if not os.path.exists(path):
        print "The training file \'%s\' does not exists. Try again!" % path
        sys.exit(1)
    elif not os.path.isfile(path):
        print "The training file \'%s\' is not a file. Try again!" % path
        sys.exit(1)

    # Loading training data
    print "Loading the training data..."
    trainset = np.load(path)

    # Convert training data to CRF Feature Format
    featset = pycrfsuite.ItemSequence(trainset[:, 0])
    labelset = trainset[:, 1]

    # Create a trainer
    trainer = pycrfsuite.Trainer()

    # Feeding training data to Trainer
    trainer.append(featset, labelset)

    # Set up some parameters of Trainer
    trainer.set_params({'c1': 1.0,\
                        'c2': 1e-3,\
                        'max_iterations': 50,\
                        'feature.possible_transitions': True})

    # Show parameters of Trainer
    print "######CRF Parameters######"
    params = trainer.get_params()
    for k in params:
        print k, ':', params[k]
    print "##########################"

    # Trainer progress
    print "Training: "
    trainer.train(model)

    # Saving model
    print "Saving the model into the file \'%s\'" % model
    #  * The model saved in previous step.

    # Finished?
    print "DONE!!"
