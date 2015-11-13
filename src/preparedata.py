import os
import io
import sys
import getopt
import re
#import string

def convertTagYN(sentence):
    result = ""
    # Word tokenize (simple based on space)
    words = sentence.split(' ')
    for word in words:
        chars = word.split('_') # Character is tieng in Vietnamese language

        for i in range(len(chars) - 1):
            chars[i] += "\tY"
        chars[-1] += "\tN"

        result += "\n".join(char for char in chars)
        result += "\n"
    return result

def convertTagBIO(sentence):
    result = ""
    # Word tokenize (simple based on space)
    words = sentence.split(' ')
    for word in words:
        chars = word.split('_') # Character is tieng in Vietnamese language

        if len(chars) == 1:
            chars[0] += "\tO"
        else:
            chars[0] += "\tB"
            for i in range(1, len(chars)):
                chars[i] += "\tI"

        result += "\n".join(char for char in chars)
        result += "\n"
    return result

def convertTagBEMS(sentence):
    result = ""
    # Word tokenize (simple based on space)
    words = sentence.split(' ')
    for word in words:
        chars = word.split('_') # Character is tieng in Vietnamese language

        if len(chars) == 1:
            chars[0] += "\tS"
        else:
            chars[0] += "\tB"
            for i in range(1, len(chars) - 2):
                chars[i] += "\tM"
            chars[-1] += "\tE"

        result += "\n".join(char for char in chars)
        result += "\n"
    return result

def prepareData(path, isDir=False, tagset="YN"):
    if isDir:
        print "Prepare data from the directory: %s" % path
    else:
        print "Prepare data from the file: %s" % path
        fread = io.open(path, 'r', encoding='utf8')
        if tagset == "YN":
            fwrite = io.open(path + ".%s.pdata" % tagset, 'w', encoding='utf8')
            for sentence in fread:
                sentence = re.sub(r'\r', '', sentence)
                sentence = re.sub(r'\n', '', sentence)
                st = convertTagYN(sentence)
                fwrite.write(st + "\n")
            fwrite.close()
        elif tagset == "BIO":
            fwrite = io.open(path + ".%s.pdata" % tagset, 'w', encoding='utf8')
            for sentence in fread:
                sentence = re.sub(r'\r', '', sentence)
                sentence = re.sub(r'\n', '', sentence)
                st = convertTagBIO(sentence)
                fwrite.write(st + "\n")
            fwrite.close()
        elif tagset == "BEMS":
            fwrite = io.open(path + ".%s.pdata" % tagset, 'w', encoding='utf8')
            for sentence in fread:
                sentence = re.sub(r'\r', '', sentence)
                sentence = re.sub(r'\n', '', sentence)
                st = convertTagBEMS(sentence)
                fwrite.write(st + "\n")
            fwrite.close()
        else:
#            print "We do not support the tagset: %s" % tagset
            fread.close()
            raise ValueError("We do not support the tagset: ", tagset)

        fread.close()

if __name__ == '__main__':
    """
    Usage: python preparedata.py -t <tagset> path/to/corpus
    """

    path = ""
    tagset = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ht:", ["tagset="])
    except getopt.GetoptError:
        print "Usage: python preparedata.py -t <tagset> path/to/corpus"
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print "Usage: python preparedata.py -t <tagset> path/to/corpus"
            sys.exit(1)
        elif opt in ("-t", "--tagset"):
            tagset = arg

    if len(args) > 0:
        path = args[0]
    else:
        print "Usage: python preparedata.py -t <tagset> path/to/corpus"
        sys.exit(2)

    # Check path is file or directory?
    isDir = False
    if os.path.isdir(path):
        isDir = True

    # Preparing data
    try:
        prepareData(path, isDir, tagset)
    except ValueError as ve:
        print ve.args[0] + ve.args[1]
        sys.exit(2)

    print "DONE!!!"

