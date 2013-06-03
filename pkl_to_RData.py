#!/usr/bin/python
"""Wrapper to convert pkl to txt, then to RData in a single script.

USE:
/usr/bin/time python $HOME/source_code/pkl_txt_RData/pkl_to_RData.py pkl_fname=$HOME/brca/GSE31448/GSE31448.SCAN.pkl.DCOR.values.pkl row_fname=$HOME/brca/GSE31448/normed/GSE31448.SCAN.tab col_fname=$HOME/brca/GSE31448/normed/GSE31448.SCAN.tab outdir=$HOME/brca/GSE31448/
"""
import sys,os
import pkl_to_txt
import subprocess
from subprocess import Popen, PIPE, STDOUT

CORRECT_NA = 'cn <- colnames(M); cn[is.na(cn)] <- "NA"; colnames(M) <- cn'

R_TMP = open(os.path.join(os.path.dirname(__file__),"txt_to_RData.R.tmp")).read()
DIR = os.path.dirname(__file__)

def main(correct_na=True, **argv):
  tab_fname = pkl_to_txt.main(**argv)
  R_fname = tab_fname + ".RData"

  print "Converting to RData binary object..."
  print "Expected R object file name: %s" % R_fname
  # hack to fix column names renamed to <NA> if the gene name is "NA"
  if correct_na:
    cn = CORRECT_NA
  else:
    cn = ""
  r_script = R_TMP % {'fin':tab_fname, 'fout':R_fname, 'correct_na':cn}
  print r_script
  p = Popen(["R", "--vanilla", "--slave"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
  print p.communicate(input=r_script)
  p.stdin.close()
  return R_fname
  

if __name__ == "__main__":
  argv = dict([s.split('=') for s in sys.argv[1:]])
  print argv
  main(**argv)
