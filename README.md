# Transcripts for Ultraschall

# Install
To use, first install conda:

```bash
#!/bin/bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

Then run `install_environment.sh`.

To activate this environment, use
`conda activate transcripts`

 To deactivate an active environment, use
`conda deactivate`

# Import German Common Voice Data

To download Mozilla Common Voice dataset for german language, run
`python3 bin/download_corpus_de.py`

Afterwards there should be a folder named "corpora/de" in your root project folder, which contains two files:

- clips.tsv.zip   - zip archive of a tab-seperated file containing all sentences and representing main training data
- de.zip          - zip archive of all german-recorded mp3-files