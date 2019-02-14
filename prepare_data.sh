#!/bin/bash

COLOR_RED='\033[0;31m'
COLOR_YELLOW='\033[1;33m'
COLOR_GREEN='\033[32m'
COLOR_RESET='\033[0m'

error() {
  echo -e "${COLOR_RED}[ERROR] $1$COLOR_RESET"
}

warning() {
  echo -e "${COLOR_YELLOW}[WARING] $1$COLOR_RESET"
}

info() {
  echo -e "${COLOR_GREEN}[INFO] $1$COLOR_RESET"
}

info "Activating python environment"
current_python=$(which python)
if ! [[ $current_python =~ ^.*transcripts/bin/python$ ]]; then
  source activate transcripts
fi

info "Downloading Mozilla Common Voice corpus"
python bin/download_corpus_de.py

info "Extracting de-lang from corpus"
python bin/create_corpus_de.py

info "Preparing DeepSpeech input data"
python bin/import_cv_de.py

info "Downloading vocab corpus and generating language model"
python bin/create_language_model_de.py