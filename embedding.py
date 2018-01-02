# -*- coding: utf-8 -*-

import os
import random
import pickle


def make_mini_embed(save_dir, embed_path, embed_name, word2id):
    assert os.path.isdir(save_dir)
    assert os.path.isfile(embed_path)
    output = open(os.path.join(save_dir, embed_name), "w+", encoding='utf-8')
    with open(embed_path, encoding="utf-8") as f:
        hang = 0
        count = 0
        find = 0
        for line in f:
            line = line.strip()
            if hang == 0 or line == '' or len(line) == 0:
                hang = hang + 1
            else:
                strings = line.split(' ')
                if strings[0] in word2id:
                    output.write(line + '\n')
                    output.flush()
                    find += 1
                count += 1
    output.close()
    print("find:", find)
    print("not find", len(word2id) - find)
    print("word", len(word2id))
    print("all:", count)


def create_embedding(embed_path, pkl_path, pkl_name, embed_dim, id2word):
    assert os.path.isfile(embed_path)
    embed_f = open(embed_path, encoding="utf-8")
    m_dict = {}
    for idx, line in enumerate(embed_f.readlines()):
        if not (line == '' or len(line) == 0):
            strings = line.split(' ')
            m_dict[strings[0]] = [float(i) for idx2, i in enumerate(strings) if not idx2 == 0]
    embed_f.close()

    m_embed = []
    not_found = 0
    for idx in range(len(id2word)):
        if id2word[idx] in m_dict:
            m_embed.append(m_dict[id2word[idx]])
        else:
            not_found += 1
            if idx == 1:
                m_embed.append([0 for _ in range(embed_dim)])
            else:
                m_embed.append([round(random.uniform(-0.25, 0.25), 6) for _ in range(embed_dim)])

    print('-------')
    print('all', len(id2word))
    print('not found:', not_found)
    print('ratio:', not_found / len(id2word))
    # m_embedding = torch.from_numpy(numpy.array(m_embed)).type(torch.DoubleTensor)

    f = open(os.path.join(pkl_path, pkl_name), 'wb+')
    pickle.dump(m_embed, f)
    f.close()
