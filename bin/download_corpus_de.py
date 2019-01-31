#!/usr/bin/env python
import boto3
import botocore
import progressbar
from botocore import UNSIGNED
from botocore.client import Config
from os import path, makedirs
from zipfile import ZipFile

REGION_NAME = 'us-east-2'
BUCKET_NAME = 'common-voice-data-download'
FILES_TO_DOWNLOAD = [
  {'filename': 'clips.tsv.zip', 'targetfolder': 'corpora'},
  {'filename': 'de.zip', 'targetfolder': 'corpora/de/audio'},
]

def _maybe_download_file(s3client, filelist, targetfolder):
  target_path = path.abspath(targetfolder)
  if not path.exists(target_path):
    print("Creating diretory {}".format(target_path))
    makedirs(target_path)

  for fileentry in filelist:
    filename = fileentry["Key"].split('/')[-1]
    filepath = path.join(target_path, filename)
    try:
      widgets = ['Download {}: '.format(filename), progressbar.Percentage(), ' ', progressbar.Bar(), ' ', progressbar.ETA(), ' Rate: ',  progressbar.FileTransferSpeed()]
      bar = progressbar.ProgressBar(widgets=widgets).start(max_value=fileentry["Size"], init=True)
      s3client.download_file(BUCKET_NAME, fileentry["Key"], filepath, Callback=lambda d: bar.update(bar.previous_value + d))
      bar.finish()
    except botocore.exceptions.ClientError as e:
      if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
      elif e.response['Error']['Code'] == "403":
        continue
      else:
        print("Error during download. Abort.")
        continue     
    
    _extract_file(filepath, targetfolder)

def _extract_file(filepath, targetfolder):
  print("Extracting {}...".format(filepath))
  with ZipFile(filepath, 'r') as zipObj:
    zipObj.extractall(path=targetfolder)

def _get_last_modified(obj):
  return int(obj['LastModified'].strftime('%s'))

def _is_executed_from_root_dir():
  check = True
  if not path.exists("README.md"):
    print("ERROR: Please exec script from root folder! (i.e. \"python bin/download_corpus_de.py\")")
    check = False

  return check

if __name__ == "__main__":
  if _is_executed_from_root_dir():
    s3 = boto3.client('s3', region_name=REGION_NAME, config=Config(signature_version=UNSIGNED))
    objs = s3.list_objects_v2(Bucket=BUCKET_NAME)['Contents']

    for fileentry in FILES_TO_DOWNLOAD:
      filename = fileentry["filename"]
      targetfolder = fileentry["targetfolder"]
      print("Trying to download {}".format(filename))
      filelist = [{"Key": obj['Key'], "Size": int(obj['Size'])} for obj in sorted(objs, key=_get_last_modified) if filename in obj['Key'] and int(obj['Size']) > 100000000]
      # only include files with resonable size (>100MB) in list to suppress errors
      _maybe_download_file(s3, filelist, targetfolder)
