__author__ = 'HyNguyen'

import numpy as np
import sys
import codecs
import matplotlib.pyplot as plt
import argparse
import time

if __name__ == '__main__':

    """
    Usage: evaluatedata.py
    """

    parser = argparse.ArgumentParser(description='Parse process ')
    parser.add_argument('-fi', required=True, type = str)
    args = parser.parse_args()

    dir_input = args.fi

    start = time.clock()

    counts = [0] * 255

    fi = codecs.open(filename=dir_input, mode='r', encoding='utf-8')
    lines = fi.readlines()

    for line in lines:
        counts[line.count(" ")] +=1

    end = time.clock()


    plt.plot(range(0, 255, 1),counts,'r-',label = 'Word count')

    plt.legend()
    plt.show()

    sys.stdout.write("Time for preparing data: " + str(end - start) + "second \n")

