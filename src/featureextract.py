import os
import sys
import io
import getopt
#from dateutil.parser import parser as dateparser
import datetime
import string
import re
import numpy as np

#################ORTHOGRAPHIC-FEATURE########################
def isDate(word):
    result = False
    format = ['%d-%m',\
              '%d/%m',\
              '%d.%m',\
              '%m-%y',\
              '%m/%y',\
              '%m.%y',\
              '%d-%m-%y',\
              '%d/%m/%y',\
              '%d.%m.%y']
    for f in format:
        try:
            datetime.datetime.strptime(word, f)
            return {'isDate': True}
        except ValueError:
            result = False

    return {'isDate': result}

def isTime(word):
    result = False
    format = ['%H:%M',\
              '%H:%M:%S',\
              '%Hh%M']
    for f in format:
        try:
            datetime.datetime.strptime(word, f)
            return {'isTime': True}
        except ValueError:
            result = False

    return {'isTime': result}

def isNumber(word):
    result = False

    try:
        float(word)
        return {'isNumber': True}
    except ValueError:
        result = False

    return {'isNumber': result}

def isPunctuation(word):
    result = word in string.punctuation
    return {'isPunc': result}

def isFirstCap(word):
    result = word[0].upper() == word[0]
    return {'isFirstCap': result}

def isAllCap(word):
    result = word.upper() == word
    return {'isAllCap': result}

def orthographicFeature(word):
    result = {}

    # Add feature
    # Update feature list in future
    result.update(isDate(word))
    result.update(isTime(word))
    result.update(isNumber(word))
    result.update(isPunctuation(word))
    result.update(isFirstCap(word))
    result.update(isAllCap(word))

    return result
#############################################################

#######################CONTEXT-FEATURE#######################

def contextFeature(word, sentence, curIndex):
    result = {}
    # Current character
    result.update({'curChar': word})
    # Two previous and next characters
    mSentence = [("<s>", "<s>")]*2
    mSentence += sentence
    mSentence += [("<\s>", "<\s>")]*2
    pattern = ""
    for i in [-2, -1, 1, 2]:
        pattern += mSentence[curIndex + 2 + i][0] + " "
    pattern = pattern[0:-1]
    result.update({'twoprenexChars': pattern})
    # One previous and next characters
    pattern = ""
    for i in [-1, 1]:
        pattern += mSentence[curIndex + 1 + i][0] + " "
    pattern = pattern[0:-1]
    result.update({'oneprenexChars': pattern})
    #TODO: Confirm later?
#    # Two previous tags
#    pattern = ""
#    for i in [-2, -1]:
#        pattern += mSentence[curIndex + 2 +i][1] + " "
#    pattern = pattern[0:-1]
#    result.update({'twopreTags':pattern})

    return result

#############################################################

def featureextract(path):
    result = []
    feat = {}
    fread = io.open(path, 'r', encoding='utf8')
    sentence = []
    sys.stdout.write("Processing: ")
    sys.stdout.flush()
    idx = 0
    for wordtag in fread:
        wordtag = re.sub(r'\r', '', wordtag)
        wordtag = re.sub(r'\n', '', wordtag)
        if wordtag == "":       # End of a sentence
            idx += 1
            if idx % 1000 == 0:
                sys.stdout.write(".")
                sys.stdout.flush()
            for i in range(len(sentence)):
                # Get feature for single character
                try:
                    feat.update(orthographicFeature(sentence[i][0]))
                except:
                    print "---> ", idx
                    print(sentence)
                # Get feature from characters around
                feat.update(contextFeature(sentence[i][0], sentence, i))
                # Make feat + tag
                result.append((feat, sentence[i][1]))
                feat = {}
            sentence = []       # Reset array
        else:
            word, tag = wordtag.split('\t')
            sentence.append((word, tag))

    # Process the last sentence in data
    for i in range(len(sentence)):
        # Get feature for single character
        feat.update(orthographicFeature(sentence[i][0]))
        # Get feature from characters around
        feat.update(contextFeature(sentence[i][0], sentence, i))
        # Make feat + tag
        result.append((feat, sentence[i][1]))
        feat = {}
    sentence = []       # Reset array

    return result

if __name__ == "__main__":
    """
    Usage: python featureextract.py path/to/corpus
    """

    path = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h")
    except getopt.GetoptError:
        print "Usage: python featureextract.py path/to/corpus"
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print "Usage: python featureextract.py path/to/corpus"
            sys.exit(0)

    if len(args) > 0:
        path = args[0]
    else:
        print "Usage: python featureextract.py path/to/corpus"
        sys.exit(2)

    # Check file to exist?
    if not os.path.exists(path):
        print "The path \'%s\' is not exists. Try again!"
        sys.exit(2)
    elif not os.path.isfile(path):
        print "The path \'%s\' is not a file. Try again!"
        sys.exit(2)

    # Feature extract
    print "Feature extracting the corpus: %s" % path
    featset = featureextract(path)

    # DEBUG
    #for i in range(20):
    #    print data[i]

    # Save to numpy format file
    print "\nSave data into the file: %s" % path + ".feat.npy"
    np.save(path + ".feat.npy", \
            np.array(featset, dtype=object))

    # Finished?
    print "DONE!!"
