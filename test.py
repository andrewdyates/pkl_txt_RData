#!/usr/bin/python
"""
python pkl_to_RData.py pkl_fname=test.pkl row_fname=test_list.txt col_fname=test_list.txt outdir=$HOME/code/pkl_txt_RData
"""
import numpy as np
import cPickle as pkl
M = np.arange(9).reshape((3,3))
pkl.dump(M, open("test.pkl","w"))
