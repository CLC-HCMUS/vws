__author__ = 'HyNguyen'

import codecs

if __name__ == "__main__":

    dir_input = "corpus/VCL_test.txt"
    dir_ouput = "corpus/VCL_test.txt.pre"

    fi = codecs.open(filename=dir_ouput,mode='r', encoding="utf-8")
    lines = fi.readlines()

    count = 0
    for line in lines:
        try:
            words, tags = line.split('\t')
            words = words.split()
            tags = tags.split()
            if len(words) != len(tags):
                print(line)
                print(words)
                print(tags)
                print('\n')
        except:
            print (line)
    fi.close()