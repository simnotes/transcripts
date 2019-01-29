#!/bin/bash

COLOR_RED='\033[0;31m'
COLOR_YELLOW='\033[1;33m'
COLOR_RESET='\033[0m'

error() {
  echo -e "${COLOR_RED}[ERROR] $1$COLOR_RESET"
}

warning() {
  echo -e "${COLOR_YELLOW}[WARING] $1$COLOR_RESET"
}

info() {
  echo -e "[INFO] $1$COLOR_RESET"
}

# install environment
env_already_installed=$(conda env list | grep transcripts | wc -l)
if [ "$env_already_installed" -eq "1" ]; then
  info "Update conda environment..."
  conda env update -f environment.yml
else
  info "Install new conda environment..."
  conda env create -f environment.yml
fi




