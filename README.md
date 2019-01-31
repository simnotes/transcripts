# Transcripts for Ultraschall

You may use the following repository to download Mozilla Common Voice data and prepare downloaded data for use with Mozilla DeepSpeech.

Only tested on Ubuntu 18.04 / 18.10.

## Install

To use, first install conda:

```bash
#!/bin/bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

and make sure to have git installed and properly setup to use with github.com.
Then run `install_environment.sh`.

To activate this environment, use
`conda activate transcripts`

 To deactivate an active environment, use
`conda deactivate`

### Installed dependencies:

Needed for getting files:

- git
- git-lfs

Needed for converting mp3-files to wav

- sox
- libsox-fmt-mp3

Needed for installing kenLM and building language model

- zlib1g-dev 
- libbz2-dev
- liblzma-dev
- libeigen3-dev
- libboost1.65-all-dev
- cmake

Needed python packages (will get installed to conda environment 'transcripts'):

- numpy
- pandas
- jupyter
- scipy
- matplotlib
- boto3
- progressbar2
- swifter
- sox

## Import German Common Voice Data

To download Mozilla Common Voice dataset for german language, run
`python3 bin/download_corpus_de.py`

Afterwards there should be a folder named "corpora/de" in your root project folder, which contains two files:

- clips.tsv.zip   - zip archive of a tab-seperated file containing all sentences and representing main training data
- de.zip          - zip archive of all german-recorded mp3-files