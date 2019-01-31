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

info "Install git..."
sudo apt-get update

info "Install additional libraries for converting mp3 to wav..."
sudo apt-get install -y sox libsox-fmt-mp3

# install python environment
env_already_installed=$(conda env list | grep transcripts | wc -l)
if [ "$env_already_installed" -eq "1" ]; then
  info "Update conda environment..."
  conda env update -f environment.yml
else
  info "Install new conda environment..."
  conda env create -f environment.yml
fi

info "Install additional packages to environment..."
source activate transcripts
pip install swifter sox

# CorporaCreator
info "Install Mozilla CorporaCreator..."
mkdir -p external
cd external
git clone git@github.com:mozilla/CorporaCreator.git
cd CorporaCreator
python setup.py install
cd ../..

# kenLM
info "Install additional libraries for creating language model (kenLM)..."
sudo apt install -y zlib1g-dev libbz2-dev liblzma-dev libeigen3-dev libboost1.65-all-dev cmake

info "Installing kenLM (for building language model)..."
mkdir -p external
cd external
git clone https://github.com/kpu/kenlm
mkdir -p kenlm/build
cd kenlm/build
cmake ..
sudo make -j 4 install
cd ../../..

info "\n\nYou may now activate your environment using:\n\n  $ conda activate transcripts\n\nHappy coding!"
