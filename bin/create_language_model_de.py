#!/usr/bin/env python
import io
import gzip
import progressbar
import requests
import shutil
import subprocess
from os import path, makedirs, remove

TARGET_PATH = "corpora/de/lm"
FILE_URL = "http://ltdata1.informatik.uni-hamburg.de/kaldi_tuda_de/German_sentences_8mil_filtered_maryfied.txt.gz"
CHUNK_SIZE = 512

def _download_file(target_path, url):
  if not path.exists(target_path):
    print("Creating diretory {}".format(target_path))
    makedirs(target_path)

  filename = url.split('/')[-1]
  filepath = path.abspath(path.join(target_path, filename))

  print("Downloading...")
  r = requests.get(url, allow_redirects=True, stream=True)
  filesize = int(r.headers['content-length'])
  
  widgets = [
        'Download ', filename,
        ': ', progressbar.Percentage(),
        ' ', progressbar.Bar(),
        ' ', progressbar.ETA(),
        ' ', progressbar.FileTransferSpeed(),
    ]
  bar = progressbar.ProgressBar(widgets=widgets, max_value=filesize).start()

  with open(filepath, 'wb') as f:
    for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
      f.write(chunk)
      bar.update(bar.previous_value + CHUNK_SIZE)

  bar.finish()

  return filepath

def _extract_file(target_path, filepath):
  if not path.exists(filepath):
    print("[ERROR] File {} is missing.".format(filepath))
    raise SystemExit

  print("Decompressing & lower-casing lines...")
  file_out = "vocab.txt"
  file_out_path = path.abspath(path.join(target_path, file_out))

  with open(file_out_path, 'w', encoding='utf-8') as f_out:
    with io.TextIOWrapper(io.BufferedReader(gzip.open(filepath)), encoding='utf8') as f_in:
      for line in f_in:
          f_out.write(line.lower())

  return file_out_path

def _build_language_model(target_path, filepath):
  if not path.exists(filepath):
    print("[ERROR] File {} is missing.".format(filepath))
    raise SystemExit

  print("Building language model...")
  file_out = "lm.arpa"
  file_out_path = path.abspath(path.join(target_path, file_out))

  subprocess.call([
    "lmplz",
    "--order", "5",
    "--temp_prefix", "/tmp/",
    "--memory", "50%",
    "--text", filepath,
    "--arpa", file_out_path,
    "--prune", "0", "0", "0", "1",
  ])

  return file_out_path

def _build_binary_language_model(target_path, filepath):
  if not path.exists(filepath):
    print("[ERROR] File {} is missing.".format(filepath))
    raise SystemExit

  print("Building binary language model...")
  file_out = "lm.binary"
  file_out_path = path.abspath(path.join(target_path, file_out))

  subprocess.call([
    "build_binary",
    "-a", "255",
    "-q", "8",
    "trie",
    filepath,
    file_out_path,
  ])

  return file_out_path

def _cleanup_files(filelist):
  print("Removing temporary files...")
  for f in filelist:
    if path.exists(f):
      remove(f)

def _is_executed_from_root_dir():
  check = True
  if not path.exists("README.md"):
    print("ERROR: Please exec script from root folder! (i.e. \"python bin/download_corpus_de.py\")")
    check = False
  return check

if __name__ == "__main__":
  if _is_executed_from_root_dir():
    downloaded_file = _download_file(TARGET_PATH, FILE_URL)
    extracted_file = _extract_file(TARGET_PATH, downloaded_file)
    lm_file = _build_language_model(TARGET_PATH, extracted_file)
    lm_binary_file = _build_binary_language_model(TARGET_PATH, lm_file)
    
    _cleanup_files([downloaded_file, extracted_file, lm_file])
