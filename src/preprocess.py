import io
import os
import sys
import re

def eraseDoubleChar(setence, char):
    result = ""
    if char != '' and setence != "":
        p = r'%c+' % char
        result = re.sub(p, char, setence)
        return result
    else:
        return None

def preprocess(path, isDir=False):
    # Open
    if isDir:
        print "Pre-processing files in the directory: %s" % path
    else:
        print "Pre-processing file: %s" % path
        fread = io.open(path, 'r', encoding='utf8')
        fwrite = io.open(path + ".pre", 'w', encoding='utf8')
        for sentence in fread:
            # Erasing newline character in Window format
            s = re.sub(r'\r', '', sentence)
            s = re.sub(r'\n', '', s)
            # Checking whether the symbol in the end of line is space or not?
            if s[-1] == ' ':
                s = s[0:-1]
            # Erasing more space, more underscore
            s = eraseDoubleChar(s, ' ')
            s = eraseDoubleChar(s, '_')
            # ...

            # Writing the pre-processed sentence.
            fwrite.write(s + "\n")

        fread.close()
        fwrite.close()

if __name__ == '__main__':
    """
    Usage: python preprocess.py path/to/corpus
    """

    path = ""
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        print "Usage: preprocess.py path/to/corpus"
        sys.exit(0)

    # Check path is a file or directory?
    isDir = False
    if os.path.isdir(path):
        isDir = True

    # Call preprocess
    preprocess(path, isDir)

    # Finished?
    print "DONE!!"
