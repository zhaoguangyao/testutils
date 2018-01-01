# -*- coding: utf-8 -*-

import re
import random

random.seed(66)


class Example(object):
    def __init__(self, sequence, label):
        self.sequence = sequence
        self.label = label


# this class can be rewrite for different kinds of corpus
def clean_sequence(string):
    # string = string.lower()
    # string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    # string = re.sub(r"\'s", " \'s", string)
    # string = re.sub(r"\'ve", " \'ve", string)
    # string = re.sub(r"n\'t", " n\'t", string)
    # string = re.sub(r"\'re", " \'re", string)
    # string = re.sub(r"\'d", " \'d", string)
    # string = re.sub(r"\'ll", " \'ll", string)
    # string = re.sub(r",", " , ", string)
    # string = re.sub(r"!", " ! ", string)
    # string = re.sub(r"\(", " \( ", string)
    # string = re.sub(r"\)", " \) ", string)
    # string = re.sub(r"\?", " \? ", string)
    # string = re.sub(r"\s{2,}", " ", string)
    return string.strip()


class Examples(object):
    def __init__(self, seq_path, label_num, shuffle=True):
        self.examples = []
        f = open(seq_path, encoding='utf-8').readlines()
        if label_num == 2:
            for line in f:
                sequence = []
                end = line.find('|')
                text = clean_sequence(line[:end])
                if line[-2] == '0' or line[-2] == '1':
                    label = "negative"
                elif line[-2] == '3' or line[-2] == '4':
                    label = "positive"
                else:
                    continue
                strings = text.split(' ')
                for word in strings:
                    sequence.append(word)
                self.examples.append(Example(sequence, label))
        elif label_num == 5:
            pass
        if shuffle:
            random.shuffle(self.examples)
