# -*- coding: utf-8 -*-

import os
import pickle

from . import embedding
from .examples import SSTExamples
from .vocabulary import Vocabulary
from .batch import MyIterator

import torch
import numpy


class DataSets(object):
    def __init__(self, corpus_path, label_num, embedding_dim, batch_size,
                 pkl_path=None, pkl_name=None,
                 embedding_file=None, embedding_name=None,
                 train=None):

        shuffle_example = True
        shuffle_batch = True
        shuffle_iterators = True
        self.embedding = None

        # one sentence saved as Example
        self.examples = SSTExamples(corpus_path, label_num, shuffle_example).examples

        # if do not has train set, making train set
        if train is None:
            self.vocabulary_text = Vocabulary.make_vocabulary_by_text([self.examples])
            self.vocabulary_label = Vocabulary.make_vocabulary_by_label([self.examples])

            # if has embedding data, like glove
            if embedding_file:
                # if has pre-training embedding(such as glove),
                # (train,dev,and test) can be saved as small file for saving time
                pkl = os.path.join(pkl_path, pkl_name)
                if os.path.isfile(pkl) is False:
                    if os.path.isfile(embedding_file):
                        embedding.make_mini_embed(pkl_path, embedding_file, embedding_name, self.vocabulary_text.word2id)
                    else:
                        print("not find embedding corpus")
                        exit()
                    id2word = self.vocabulary_text.id2word
                    embedding.create_embedding(os.path.join(pkl_path, embedding_name), pkl_path, pkl_name, embedding_dim, id2word)
                else:
                    print("has mini embedding ")

                plk_f = open(pkl, 'rb+')
                m_embed = pickle.load(plk_f)
                self.embedding = torch.from_numpy(numpy.array(m_embed)).type(torch.DoubleTensor)
                plk_f.close()
            else:
                pass

            # get iterator batch
            self.iterator = MyIterator(batch_size, self.examples, self.vocabulary_text, self.vocabulary_label,
                                       shuffle_batch=shuffle_batch, shuffle_iterators=shuffle_iterators).iterators
        else:
            # get iterator batch
            self.iterator = MyIterator(batch_size, self.examples, train.vocabulary_text, train.vocabulary_label,
                                       shuffle_batch=shuffle_batch, shuffle_iterators=shuffle_iterators).iterators


# example
if __name__ == "__main__":
    data = DataSets("../data/ten.dat", 300, 1)
