#!/usr/bin/python
"""Wrapper to convert pkl to txt, then to RData in a single script."""
import sys,os
import pkl_to_txt
import subprocess

DIR = os.path.dirname(__file__)

def main(**argv):
  tab_fname = pkl_to_txt.main(**argv)
  R_fname = tab_fname + ".RData"
  cmd = "Rscript %s/txt_to_RData.R %s" % (DIR, tab_fname)
  print cmd
  rcode = subprocess.call(cmd, shell=True)
  print "RScript Return Code: ", rcode
  print "Expected R object file name: %s" % R_fname
  return R_fname

if __name__ == "__main__":
  argv = dict([s.split('=') for s in sys.argv[1:]])
  print argv
  main(**argv)
