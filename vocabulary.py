# -*- coding: utf-8 -*-


class Vocabulary(object):
    def __init__(self, id2word, word2id):
        self.id2word = id2word
        self.word2id = word2id

    @classmethod
    def make_vocabulary_by_text(cls, all_examples):
        frequency = dict()
        id2word = {}
        word2id = {}
        for examples in all_examples:
            for e in examples:
                for word in e.sequence:
                    if word in frequency:
                        frequency[word] += 1
                    else:
                        frequency[word] = 1
        all_words = sorted(frequency.items(), key=lambda t: t[1], reverse=True)
        id2word[0] = "<unknown>"
        word2id["<unknown>"] = 0
        id2word[1] = "<padding>"
        word2id["<padding>"] = 1
        for idx, word in enumerate(all_words):
            id2word[idx + 2] = word[0]
            word2id[word[0]] = idx + 2
        return cls(id2word, word2id)

    @classmethod
    def make_vocabulary_by_label(cls, all_examples):
        frequency = dict()
        id2word = {}
        word2id = {}
        for examples in all_examples:
            for e in examples:
                if e.label in frequency:
                    frequency[e.label] += 1
                else:
                    frequency[e.label] = 1
        all_words = sorted(frequency.items(), key=lambda t: t[1], reverse=True)
        for idx, word in enumerate(all_words):
            id2word[idx] = word[0]
            word2id[word[0]] = idx
        return cls(id2word, word2id)
