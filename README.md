# textutils
process corpus

this can be used for sst , just for what I have experience

# parameters

 - corpus_path: corpus_path.
 - label_num: the number of label. (sst has 5 labels).
 - pkl_path: glove.840B.300d.txt size is 5G, it is too big to use every trainning, so i use pickle to save as a small file
        for saving time, this is saving path.
 - pkl_name: same as above, this is saving name.
 - embedding_file: Choose to use which one embedding, this is embedding path. (d:/glove.840B.300d.txt).
 - embedding_name: same as above, this is embedding name.
 - embedding_dim: the embedding you choose dim.
 - batch_size: batch size.
 - train=None: when generate train set, this is None; when generate dev set and test set, this is train set.
