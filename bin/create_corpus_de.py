#!/usr/bin/env python
import subprocess
from os import path

CORPUS_FILE_PATH = "corpora/clips.tsv"

def _is_executed_from_root_dir():
  check = True
  if not path.exists("README.md"):
    print("ERROR: Please exec script from root folder! (i.e. \"python bin/create_corpus_de.py\")")
    check = False
  return check

if __name__ == "__main__":
  if _is_executed_from_root_dir():
    if not path.exists(CORPUS_FILE_PATH):
        print("File {} not found. Aborting...".format(CORPUS_FILE_PATH))
        raise SystemExit
    subprocess.run(["create-corpora", "-f", CORPUS_FILE_PATH, "-d", "corpora", "-l", "de", "-s", "3"])
    