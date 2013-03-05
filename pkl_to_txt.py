#!/usr/bin/python
"""Load pickled numpy matrix, remove non-significant rows and columns, save as text.

EXAMPLE:

$ python $HOME/pymod/pkl_txt_RData/pkl_to_txt.py pkl_fname=/fs/lustre/osu6683/gse15745_feb27_dep/all_aligned_dual/compiled_dep_matrices/gibbs.meth.all.aligned.psb.corr.feb-15-2013.pkl_gibbs.mrna.all.aligned.psb.corr.feb-15-2013.pkl.DCOR.values.pkl row_fname=$HOME/gibbs_feb16_cleaned_data/gibbs.meth.all.aligned.psb.corr.feb-15-2013.tab col_fname=$HOME/gibbs_feb16_cleaned_data/gibbs.mrna.all.aligned.psb.corr.feb-15-2013.tab outdir=/fs/lustre/osu6683
"""
import matrix_io as mio
from lab_util import *
import cPickle as pickle
import sys
import os
import datetime


def main(pkl_fname=None, row_fname=None, col_fname=None, outdir=None, sig=None, doabs=False):
  """
  pkl_fname: path to pickled numpy dependency matrix
  row_fname: path to labeled text matrix with row ids, maybe col ids
  col_fname: optional path to labeled text matrix with col ids
  sig: float of minimum significance
  doabs: flag of whether to use absolute value for significance testing
  """
  assert pkl_fname and row_fname and outdir
  make_dir(outdir)
  if doabs:
    abstxt = "T"
  else:
    abstxt = "F"
  out_fname = os.path.join(outdir, os.path.basename(pkl_fname.rpartition('.')[0])+".sig=%s.abs=%s.tab"%(str(sig),str(abstxt)))
  print "Text matrix will be saved to: %s" % out_fname
  M = pickle.load(open(pkl_fname))

  # Get row and column labels.
  D_row = mio.load(row_fname)
  row_names = np.array(D_row['row_ids'])
  if col_fname is None:
    col_names = np.array(D_row['col_ids'])
  else:
    D_col = mio.load(col_fname)
    col_names = np.array(D_col['row_ids'])
  assert len(row_names) == np.size(M,0)
  assert len(col_names) == np.size(M,1)

  # Remove insignificant rows and columns; align row/col names
  original_dim = M.shape
  if sig is not None:
    sig = float(sig)
    if not doabs:
      col_max = np.amax(M,0)
      row_max = np.amax(M,1)
    else:
      col_max = np.amax(np.abs(M),0)
      row_max = np.amax(np.abs(M),1)
    M = M[row_max>=sig,:][:,col_max>=sig]
    row_names = row_names[row_max>=sig]
    col_names = col_names[col_max>=sig]
  new_dim = M.shape

  # Dump to text
  now_timestamp = datetime.datetime.now().isoformat('_')
  header = ["Generated on %s from pickled matrix file %s" % (now_timestamp, pkl_fname),
            "Original dimensions: %s, New dimensions: %s" % (original_dim, new_dim),
            "sig: %s, abs: %s" % (str(sig), str(abstxt))]
  print "\n".join(header)
  fp = open(out_fname, "w")
  mio.save(M, fp, ftype="txt", delimit_c="\t", row_ids=list(row_names), col_ids=list(col_names), headers=header)
  fp.close()
  print "Tab matrix saved to %s." % out_fname
  
  return out_fname


if __name__ == "__main__":
  argv = dict([s.split('=') for s in sys.argv[1:]])
  print argv
  main(**argv)
