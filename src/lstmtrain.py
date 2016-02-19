import io
import os
import argparse

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, TimeDistributedDense
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import GRU

from keras.preprocessing import sequence
from keras.utils import generic_utils

from utils import grouper

verbose = os.environ.get('VERBOSE', 'no') == 'yes'

def getDictionary(path2File, use_unk=True):
    wordDict = {}
    idx = 0
    with io.open(path2File, encoding='utf8') as fread:
        for sent in fread:
            lstWords = sent.split()
            for word in lstWords:
                if not wordDict.has_key(word):
                    wordDict[word] = idx
                    idx += 1
    if use_unk:
        wordDict['UNK'] = idx
    return wordDict

def getNumerialValues(path2File, dictionary):
    result = []

    with io.open(path2File, encoding='utf8') as fread:
        for line in fread:
            numLine = []
            lstItems = line.split()
            for item in lstItems:
                if dictionary.has_key(item):
                    numLine.append(dictionary[item])
                elif dictionary.has_key('UNK'):
                    numSent.append(dictionary['UNK'])
                else:
                    raise ValueError("Cannot find the numerical value of item: " + item)
            result.append(numLine)

    return result

def main():

    parser = argparse.ArgumentParser(description='Parse process ')
    parser.add_argument('-xtrain', required=True, type = str)
    parser.add_argument('-ytrain', required=True, type = str)
    parser.add_argument('-xval', required=True, type = str)
    parser.add_argument('-yval', required=True, type = str)
    parser.add_argument('-model', required=True, type=str)
    parser.add_argument('-outputdir', required=True, type=str)
    args = parser.parse_args()

    path2XTrain = args.xtrain
    path2YTrain = args.ytrain
    path2XVal = args.xval
    path2YVal = args.yval
    path2OutputDir = args.outputdir
    modelName = args.model

    nbofEpochs = 100
    maxLen = 50
    batchSize = 100
    patience = 10

    wordDict = getDictionary(path2XTrain, True)
    tagDict = getDictionary(path2YTrain, False)

    # Convert the format of input is from text to integer
    XTrain = getNumerialValues(path2XTrain, wordDict)
    # ...
    XTrain = sequence.pad_sequences(XTrain, maxLen)

    # Convert the label into numerical format
    YTrain = getNumerialValues(path2YTrain, tagDict)
    # ...
    YTrain = sequence.pad_sequences(YTrain, maxLen)
    if verbose:
        print "Loaded training data."

    # Convert the format of input is from text to integer
    XVal = getNumerialValues(path2XVal, wordDict)
    # ...
    XVal = sequence.pad_sequences(XVal, maxLen)

    # Convert the label into numerical format
    YVal = getNumerialValues(path2YVal, tagDict)
    # ...
    YVal = sequence.pad_sequences(YVal, maxLen)
    if verbose:
        print "Loaded validation data."

    #Build the network
    vocabSize = len(wordDict)
    nbofTag = len(tagDict)
    embeddingSize = 100

    model = Sequential()
    model.add(Embedding(vocabSize, embeddingSize, init='lecun_uniform'))
    model.add(GRU(embeddingSize, 50, return_sequences=True))
    model.add(TimeDistributedDense(nbofTag))
    model.add(Activation('softmax'))
    if verbose:
        print "Built the network."
    # Write network description to file
    network2JSON = model.to_json()
    with open(os.path.json(path2OutputDir, modelName +'.json'), 'w') as fwrite:
        fwrite.write(network2JSON)
    #Compile the network
    model.compile(loss='categorial_crossentropy', optimizer='rmsprop')
    if verbose:
        print "Compiled the network."
    # Training progress
    print "Training started ..."
    bestAcc = None
    bestTrainLoss = None
    wait = 0
    bestEpoch = -1
    stop = False
    for n in xrange(nbofEpochs):
        trainLossPerEpoch = 0.0
        print "Epoch %3d:" % n
        progbar = generic_utils.Progbar(len(XTrain))

        for bX, bY in zip(grouper(XTrain, batchSize), \
                          grouper(YTrain, batchSize) \
                          ):
            if bX[-1] is None:
                bX = [x for x in bX if x is not None]
            if bY[-1] is None:
                bY = [y for y in bY if y is not None]

            trainLoss = model.train_on_batch(bY, bY)

            trainLossPerEpoch += (float) (trainLoss[0] * len(bX))

            progbar.add(len(bX), values=[('train_loss', trainLoss[0])])

        # Evaluating on validation dataset
        valLoss, valAcc = model.evaluate(XVal, YVal, batch_size=100, show_accuracy=True)

        print "--> Validation Accuracy: %.4f" % (valAcc)

        if (bestAcc is None) or (valAcc > bestAcc):
            bestAcc = valAcc
            bestTrainLoss = trainLossPerEpoch / (len(XTrain) * 1.0)
            wait = 0
            bestEpoch = n
            #Save model
            model.save_weights(os.path.join(path2OutputDir, \
                                            modelName + '.hdf5' \
                                            ), \
                               overwrite=True \
                               )
        else:
            wait += 1
            if wait > patience:
                print "Patience level reached, early stop."
                print "Will stop at score ", bestTrainLoss, 'at epoch ', bestEpoch, '.'
                stop = True

        if stop:
            break


if __name__ == '__main__':
    main()
