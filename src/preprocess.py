import io
import os
import sys
import re

from xml.etree.ElementTree import iterparse

class ItemXML(object):
    def __init__(self, dict_item):
        self.content = dict_item['CONTENT']
        self.label = dict_item['LABEL']
        self.sentiment_vector_score = None

    def item_xml_from_dictionary(cls, dict_item):
        return ItemXML(dict_item)

def loadFileXML(path2File):
    """
    This function read a file XML (which is formatted by @GiaHy) and
    return the list of dictionary which have 'CONTENT', 'LABEL' in that
    'CONTENT' is a list of 'SENTENCE' and 'LABEL' is a sentiment label (positive, negative, neutral)
    """

    doc = iterparse(path2File, ('start', 'end'))
    # Skip the root element
    next(doc)

    items = []
    content = []
    label = -1

    tagStack = []
    elemStack = []

    item = None
    count = 0

    for event, elem in doc:
        if event == 'start':
            if elem.tag == 'ITEM':
                item = {}
                content.clear()
                label = -1
            tagStack.append(elem.tag)
            elemStack.append(elem)
        elif event == 'end':
            if elem.tag == 'ITEM':
                item['CONTENT'] = content
                item['LABEL'] = label
                items.append(ItemXML(item))
                count += 1
                if count % 10000 == 0:
                    print "Finished:", count
            elif elem.tag == 'SENTENCE':
                content.append(elem.text)
            elif elem.tag == 'LABEL':
                label = int(elem.text)

            try:
                tagStack.pop()
                elemStack.pop()
            except IndexError:
                pass

    return items

def saveFileXML(path2File, items):
    with io.open(path2File, 'w', encoding='utf8') as fwrite:
        fwrite.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
        fwrite.write(" <DATA> ")

        for item in items:
            fwrite.write(" <ITEM> ")
            fwrite.write(" <CONTENT> ")
            for sent in item['CONTENT']:
                fwrite.write(" <SENTENCE> ")
                fwrite.write("\n" + sent)
                fwrite.write(" </SENTENCE> ")
            fwrite.write(" </CONTENT> ")
            fwrite.write(" <LABEL> ")
            fwrite.write(item['LABEL'])
            fwrite.write(" </LABEL> ")
            fwrite.write(" </ITEM> ")

        fwrite.write(" </DATA> ")
        fwrite.close()

def eraseDoubleChar(setence, char):
    result = ""
    if char != '' and setence != "":
        p = r'%c+' % char
        result = re.sub(p, char, setence)
        return result
    else:
        return None

def preprocess(path, format='txt', isDir=False):
    # Open
    if isDir:
        print "Pre-processing files in the directory: %s" % path
    else:
        print "Pre-processing file: %s" % path
        if format == 'txt':
            fread = io.open(path, 'r', encoding='utf8')
            fwrite = io.open(path + ".pre", 'w', encoding='utf8')
            for sentence in fread:
                # Erasing the tab character
                s = re.sub(r'\t', '', sentence)
                # Erasing newline character in Window format
                s = re.sub(r'\r', '', s)
                s = re.sub(r'\n', '', s)
                # Erasing the pattern '[a-zA-Z]*_ '
                s = re.sub(r'_ ', ' ', s)

                # Checking whether the symbol in the end of line is space or not?
                if s[-1] == ' ':
                    s = s[0:-1]
                # Erasing more space, more underscore
                s = eraseDoubleChar(s, ' ')
                s = eraseDoubleChar(s, '_')
                # ...
                #
                s = re.sub(r'^ ', '', s)
                # Writing the pre-processed sentence.
                fwrite.write(s + "\n")

            fread.close()
            fwrite.close()
        elif format == 'xml':
            items = loadFileXML(path)
            for item in items:
                for i, sentence in enumerate(item['CONTENT']):
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
                    item['CONTENT'][i] = s
            # Save items into XML file.
            saveFileXML(path + ".pre")
        else:
            print "Do not support this file format: ", format

if __name__ == '__main__':
    """
    Usage: python preprocess.py <format-of-file> path/to/corpus
    """

    path = ""
    format = 'txt'
    if len(sys.argv) > 2:
        path = sys.argv[2]
        format = sys.argv[1]
    else:
        print "Usage: preprocess.py path/to/corpus"
        sys.exit(0)

    # Check path is a file or directory?
    isDir = False
    if os.path.isdir(path):
        isDir = True

    # Call preprocess
    preprocess(path, format, isDir)

    # Finished?
    print "DONE!!"
