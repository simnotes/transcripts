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

## How to use

After finishing installation process (see above), just execute `./prepare_data.sh`. After finishing, you should end up with a new folder `corpora` with following structure:

$ tree -L 2 corpora 
corpora
├── clips.tsv
├── clips.tsv.zip
└── de
    ├── audio  <- contains all the mp3s/wav-files
    ├── dev_file.csv
    ├── dev.tsv
    ├── invalid.tsv
    ├── other.tsv
    ├── test_file.csv
    ├── test.tsv
    ├── train_file.csv
    ├── train.tsv
    └── valid.tsv

You can now use train_file.csv, dev_file.csv and test_file.csv for training your model.

# TODO:

Add additional scripts to generate binary language model (via kenLM) and alphabet.txt.