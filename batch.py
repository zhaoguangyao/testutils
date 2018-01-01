# -*- coding: utf-8 -*-

import random
import numpy
import torch
from torch.autograd import Variable

random.seed(66)


class Batch(object):
    def __init__(self, text, label):
        self.text = text
        self.label = label
        self.batch_size = len(text)

    @classmethod
    def get_batch(cls, item, shuffle=False):
        max_len = 0
        for i in item:
            if len(i[0]) > max_len:
                max_len = len(i[0])
        text = []
        label = []
        if shuffle:
            random.shuffle(item)
        for i in item:
            seq = []
            for idx in range(max_len):
                if idx < len(i[0]):
                    seq.append(i[0][idx])
                else:
                    seq.append(1)
            text.append(seq)
            label.append(i[1])

        text_v = Variable(torch.from_numpy(numpy.array(text)).type(torch.LongTensor))
        label_v = Variable(torch.from_numpy(numpy.array(label)).type(torch.LongTensor))
        return cls(text_v, label_v)


class MyIterator(object):
    def __init__(self, batch_size, examples, vocabulary_text, vocabulary_label,
                 shuffle_batch=False, shuffle_iterators=False):
        self.iterators = []
        item = []
        count = 0
        for example in examples:
            text = []
            for word in example.sequence:
                if word in vocabulary_text.word2id:
                    text.append(vocabulary_text.word2id[word])
                else:
                    text.append(0)

            item.append((text, vocabulary_label.word2id[example.label]))
            count += 1
            if count % batch_size == 0 or count == len(examples):
                self.iterators.append(Batch.get_batch(item, shuffle=shuffle_batch))
                item = []

        if shuffle_iterators:
            random.shuffle(self.iterators)
