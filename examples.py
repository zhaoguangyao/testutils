# -*- coding: utf-8 -*-

import re
import copy
import random

random.seed(66)


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


# SST
class SSTExample(object):
    def __init__(self, sequence, label):
        self.sequence = copy.copy(sequence)
        self.label = copy.copy(label)


class SSTExamples(object):
    def __init__(self, seq_path, label_num, shuffle=True, if_re=False):
        self.examples = []
        self.path = seq_path
        self.shuffle = shuffle
        self.if_re = if_re

        self.label_num = label_num

    def generate_examples(self):
        f = open(self.path, encoding='utf-8').readlines()
        if self.label_num == 2:
            for line in f:
                if self.if_re:
                    line = clean_sequence(line)
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
                self.examples.append(SSTExample(sequence, label))
        elif self.label_num == 5:
            for line in f:
                if self.if_re:
                    line = clean_sequence(line)
                sequence = []
                end = line.find('|')
                text = clean_sequence(line[:end])
                if line[-2] == '0':
                    label = "strong_negative"
                elif line[-2] == '1':
                    label = "weak_negative"
                elif line[-2] == '2':
                    label = "neutral"
                elif line[-2] == '3':
                    label = "weak_positive"
                elif line[-2] == '4':
                    label = "strong_positive"
                else:
                    print("something wrong")
                    exit()
                strings = text.split(' ')
                for word in strings:
                    sequence.append(word)
                self.examples.append(SSTExample(sequence, label))
        if self.shuffle:
            random.shuffle(self.examples)
        return self.examples


# Attention Modeling for Targeted Sentiment
class ZExample(object):
    def __init__(self, sequence, target_start, target_end, label):
        self.sequence = copy.copy(sequence)
        self.target_start = target_start
        self.target_end = target_end
        self.label = label


class ZExamples(object):
    def __init__(self, path, shuffle=True, if_re=False):
        self.examples = []
        self.path = path
        self.shuffle = shuffle
        self.if_re = if_re

    def generate_examples(self):
        f = open(self.path, encoding='utf-8').readlines()
        sequence = []
        target_start = -1
        target_end = -1
        label = None
        count = 0
        isf = False
        for line in f:
            line = line.strip()
            if line == "" or len(line) == 0:
                if isf:
                    target_end = count - 1
                    isf = False
                self.examples.append(ZExample(sequence, target_start, target_end, label))
                sequence.clear()
                count = 0
            else:
                strings = line.split(' ')
                if self.if_re:
                    m_input = clean_sequence(strings[0])
                    ss = m_input.split(' ')
                    for idx in range(len(ss)):
                        sequence.append(clean_sequence(ss[idx]))
                else:
                    sequence.append(strings[0])

                if strings[1] == 'o':
                    if isf:
                        target_end = count - 1
                        isf = False
                else:
                    if strings[1][0] == 'b':
                        target_start = count
                        label = strings[1][2:]
                        isf = True
                count += 1

        if self.shuffle:
            random.shuffle(self.examples)
        return self.examples


# target include several target
class TargetExample(object):
    def __init__(self, sequence, target_start, target_end, label):
        """
            :sequence: list
            :target_start: list
            :target_end: list
            :label: list
            :because a sentence may contain several targets
        """
        self.sequence = copy.copy(sequence)
        self.target_start = copy.copy(target_start)
        self.target_end = copy.copy(target_end)
        self.label = copy.copy(label)


class TargetExamples(object):
    def __init__(self, path, shuffle, if_re=False):
        self.examples = []
        self.path = path
        self.shuffle = shuffle
        self.if_re = if_re

    def generate(self):
        f = open(self.path, encoding='utf-8').readlines()
        sentence = []
        target_starts = []
        target_ends = []
        labels = []
        word_count = 0
        now_target = False
        for line in f:
            line = line.strip()
            if line == "" or len(line) == 0:

                for i in range(len(target_starts)):
                    self.examples.append(TargetExample(sentence, target_starts[i], target_ends[i], labels[i]))
                sentence.clear()
                target_starts.clear()
                target_ends.clear()
                labels.clear()
                word_count = 0
            else:
                strings = line.split('\t')
                if self.if_re:
                    strings[0] = clean_sequence(strings[0])
                sentence.append(strings[0])
                if strings[2] == 's':
                    target_starts.append(word_count)
                    target_ends.append(word_count)
                    labels.append(strings[3])
                elif strings[2] == 'b':
                    target_starts.append(word_count)
                    labels.append(strings[3])
                    now_target = True
                elif strings[2] == 'm':
                    pass
                elif strings[2] == 'e':
                    if now_target is False:
                        print("something wrong")
                        exit()
                    else:
                        target_ends.append(word_count)
                        now_target = False
                elif strings[2] == 'o':
                    pass
                word_count += 1

        if self.shuffle:
            random.shuffle(self.examples)
        return self.examples


# Paragraph
class Paragraph(object):
    def __init__(self, sentences, label):
        self.sentences = copy.copy(sentences)
        self.label = copy.copy(label)


class ParagraphExample:
    def __init__(self, paragraph_path, sentence_path, shuffle, if_re=False):
        self.examples = []
        self.para_path = paragraph_path
        self.sentence_path = sentence_path
        self.shuffle = shuffle
        self.if_re = if_re

    def generate_paragraphs(self):
        para_file = open(self.para_path, encoding='utf-8')
        sentence_file = open(self.sentence_path, encoding='utf-8')

        sentences = []
        sentences_count = 0
        while 1:
            para = para_file.readline()
            if not para:
                break
            paras = para.split("\t")

            sentence = []
            while 1:
                line = sentence_file.readline()
                line = line.strip()
                if line == "" or len(line) == 0:
                    t = copy.copy(sentence)
                    sentences.append(t)
                    sentence.clear()

                    sentences_count += 1

                    if sentences_count == int(paras[1]):
                        self.examples.append(Paragraph(sentences, paras[2]))
                        sentences.clear()
                        sentences_count = 0
                        break
                else:
                    strings = line.split('\t')
                    sentence.append(strings[0])
        if self.shuffle:
            random.shuffle(self.examples)
        return self.examples




