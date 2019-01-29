#!/usr/bin/env python
import csv
import pandas as pd
import progressbar
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

if __name__ == "__main__":
  for currentfile in FILES_TO_PROCESS:
    print("\nProcessing {}...".format(currentfile))

    currentfile = path.join(CORPUS_FILES_PATH, currentfile)
    df = pd.read_csv(currentfile, 
      sep="\t",
      parse_dates=False,
      engine="python",
      encoding="utf-8",
      escapechar='"',
      error_bad_lines=False,
      quotechar='"',
      quoting=csv.QUOTE_NONE,)

    print("Starting conversion from mp3 to wav...")
    df[["wav_path", "wav_file_size", "status"]] = df.swifter.apply(
      lambda r: _convert_wav(AUDIO_FILES_PATH, r["path"], r["sentence"]),  axis=1
    )
    
    columns = ["wav_filename", "wav_filesize", "transcript"]
    output_df = pd.DataFrame(columns=columns)
    output_df[["wav_filename", "wav_filesize", "transcript"]] = df[
      df["status"] == "ok"].loc[:, ("wav_path", "wav_file_size", "sentence")
    ]

    csv_filename = path.splitext(currentfile)[0] + ".csv"
    output_df.to_csv(
      csv_filename, header=True
    )

    status_counts = df["status"].value_counts()
    print("Statistics for {}:\n\tOk samples: {}\n\tToo short samples: {}\n\tToo long samples: {}".format(
      currentfile,
      getattr(status_counts, "ok", 0),
      getattr(status_counts, "too_short", 0),
      getattr(status_counts, "too_long", 0)
    ))


