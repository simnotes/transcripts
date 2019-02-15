#!/usr/bin/env python
import csv
import pandas as pd
import progressbar
import re
import subprocess
import swifter
from os import path
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count
from sox import Transformer

SAMPLE_RATE = 16000
MAX_SECS = 10
CORPUS_FILES_PATH = "corpora/de"
AUDIO_FILES_PATH = "corpora/de/audio"
FILES_TO_PROCESS = ["train.tsv", "dev.tsv", "test.tsv"]

allowed_chars = set([' ', 'a', 'ä', 'b', 'c', 'd', 'e', 'f',
                     'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                     'o', 'ö', 'p', 'q', 'r', 's', 'ß', 't',
                     'u', 'ü', 'v', 'w', 'x', 'y', 'z'])
chars = ''.join(allowed_chars)
pattern = r'[^' + chars + ']'
ALPHABET_FILTER = re.compile(pattern)


def _convert_wav(path_prefix, filepath, sentence):
  wav_filename = path.splitext(filepath)[0] + ".wav"
  wav_path = path.abspath(path.join(path_prefix, wav_filename))
  mp3_path = path.abspath(path.join(path_prefix, filepath))
  _maybe_convert_wav(mp3_path, wav_path)
  frames = int(subprocess.check_output(['soxi', '-s', wav_path], stderr=subprocess.STDOUT))
  wav_file_size = path.getsize(wav_path)
  
  status = "no_status"
  
  if int(frames/SAMPLE_RATE*1000/10/2) < len(str(sentence)):
    # Excluding samples that are too short to fit the transcript
    status = "too_short"
  elif frames/SAMPLE_RATE > MAX_SECS:
    # Excluding very long samples to keep a reasonable batch-size
    status = "too_long"
  else:
    status = "ok"
  
  return pd.Series([wav_path, wav_file_size, status])
    

def _maybe_convert_wav(mp3_filename, wav_filename):
  if not path.exists(wav_filename):
    transformer = Transformer()
    transformer.convert(samplerate=SAMPLE_RATE)
    transformer.build(mp3_filename, wav_filename)


def _load_data_to_df(filename):
  filename = path.join(CORPUS_FILES_PATH, filename)
  df = pd.read_csv(filename, 
    sep="\t",
    parse_dates=False,
    engine="python",
    encoding="utf-8",
    escapechar='"',
    error_bad_lines=False,
    quotechar='"',
    quoting=csv.QUOTE_NONE,)

  return df


def _process_data_df(df):
  print("Starting conversion from mp3 to wav...")
  df[["wav_path", "wav_file_size", "status"]] = df.swifter.apply(
    lambda r: _convert_wav(AUDIO_FILES_PATH, r["path"], r["sentence"]),  axis=1
  )

  columns = ["wav_filename", "wav_filesize", "transcript"]
  output_df = pd.DataFrame(columns=columns)
  output_df[["wav_filename", "wav_filesize", "transcript"]] = df[
    df["status"] == "ok"].loc[:, ("wav_path", "wav_file_size", "sentence")
  ]

  status_counts = df["status"].value_counts()
  print("Statistics for {}:\n\tOk samples: {}\n\tToo short samples: {}\n\tToo long samples: {}".format(
    currentfile,
    getattr(status_counts, "ok", 0),
    getattr(status_counts, "too_short", 0),
    getattr(status_counts, "too_long", 0)
  ))

  return output_df


def _cleanup_sentences(sentence):
  sentence = sentence.lower()
  sentence = ALPHABET_FILTER.sub('', sentence)
  return sentence


def _cleanup_sentences_wrapper(df):
  print("Cleanup sentences...")
  df[["transcript"]] = df.swifter.apply(lambda r: _cleanup_sentences(r["transcript"]), axis=1)
  return df


def _save_df_to_csv(df, filename):
  print("Saving converted files and sentences to csv...")
  csv_filename = path.splitext(filename)[0] + "_file.csv"
  csv_filepath = path.join(CORPUS_FILES_PATH, csv_filename)
  df.to_csv(
    csv_filepath, header=True
  )

def _is_executed_from_root_dir():
  check = True
  if not path.exists("README.md"):
    print("ERROR: Please exec script from root folder! (i.e. \"python bin/import_cv_de.py\")")
    check = False
  return check

if __name__ == "__main__":
  if _is_executed_from_root_dir():
    for currentfile in FILES_TO_PROCESS:
      if not path.exists(path.join(CORPUS_FILES_PATH,currentfile)):
        print("File {} not found. Aborting...".format(currentfile))
        raise SystemExit

      print("\nProcessing {}...".format(currentfile))

      df = _load_data_to_df(currentfile)
      df = _process_data_df(df)
      df = _cleanup_sentences_wrapper(df)
      _save_df_to_csv(df, currentfile)

