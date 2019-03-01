#!/bin/bash
 
set -xe
if [ ! -f README.md ]; then
    echo "Please make sure you run this from Transcripts's top level directory."
    exit 1
fi;
 
prefix="commonvoicefull"
 
DATA_DIR="$HOME/dev/private/deepspeech/transcripts/corpora/de"
ALPHABET="$DATA_DIR/lm/alphabet.txt"
LM_BINARY="$DATA_DIR/lm/lm.binary"
LM_TRIE="$DATA_DIR/lm/trie"
TRAIN_CSV="$DATA_DIR/train_file.csv"
DEV_CSV="$DATA_DIR/dev_file.csv"
TEST_CSV="$DATA_DIR/test_file.csv"
 
BATCH_SIZE=3
 
# check directory if exist
declare -a files=(
    $ALPHABET
    $TRAIN_CSV
    $DEV_CSV
    $TEST_CSV
)
 
for file in "${files[@]}"
do
    if [ ! -f "$file" ]; then
        echo "File not found: $file"
        exit 100
    fi;
done
 
if [ -d "${COMPUTE_KEEP_DIR}" ]; then
    checkpoint_dir=$COMPUTE_KEEP_DIR
else
    checkpoint_dir=$(python -c "from xdg import BaseDirectory as xdg; print(xdg.save_data_path(\"deepspeech/$prefix\"))")
fi
 
python -u ./external/DeepSpeech/DeepSpeech.py \
  --alphabet_config_path $ALPHABET \
  --lm_binary_path $LM_BINARY \
  --lm_trie_path $LM_TRIE \
  --train_files $TRAIN_CSV \
  --dev_files $DEV_CSV \
  --test_files $TEST_CSV \
  --train_batch_size $BATCH_SIZE \
  --dev_batch_size $BATCH_SIZE \
  --test_batch_size $BATCH_SIZE \
  --n_hidden 512 \
  --learning_rate 0.0001 \
  --epoch 50 \
  --checkpoint_dir "$checkpoint_dir" \
  --export_dir "$DATA_DIR" \
  --log_level 0 \
  --summary_secs 3 \
  "$@"