#!/usr/bin/env python
import subprocess
from os import path

def _is_executed_from_root_dir():
  check = True
  if not path.exists("README.md"):
    print("ERROR: Please exec script from root folder! (i.e. \"python bin/create_corpus_de.py\")")
    check = False
  return check

if __name__ == "__main__":
  if _is_executed_from_root_dir():
    subprocess.run(["create-corpora", "-f", "corpora/clips.tsv", "-d", "corpora", "-l", "de"])
    