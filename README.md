# Installation

```bash
$ git clone https://github.com/dmalt/get_some_rest.git
$ cd get_some_rest
$ pip install --editable .
```

# Utilities

## ica_var 
Show explained variance for mne-python ICA solution

##### Examples:
```bash
$ ica_var ./MEG2016/*/*-ica.fif >> vars.txt
```

## bst2mne
Convert epochs from brainstorm protocol in .mat format to mne.Epochs object and save to a file

##### Options:

	  -s, --savename TEXT

	  --rec-type [ds|fif]

	  -i, --infosrc TEXT   file to take info from

	  --help               Show this message and exit.

##### Examples:
```bash
$ bst2mne ~/Documents/dmalt_sample_epochs/data*.mat -s ${PWD##*/}-epo.fif -i Control01_Open.ds
```

## psd2bandpower
Find [basename]-psds.npy and [basename]-freqs.npy in [PWR_DIRS], load them to compute power in a BAND and save the result to [basename][-bandname][_band]-pwr.npy

Each dir must contain only one instance of [basename]-psds.npy and [basename]-freqs.npy 


EXAMPLES:

    # Say, we have a pipeline folder with psds computed.
    # Each subfolder has psds and freqs files inside.
    # The most basic usage would be

    $ psd2bandpwr ~/pipeline/*subj_id* 8 12 
    
    # This will compute power in alpha band for each subject in ~/pipeline

    # Now assume we have two groups: controls and patients
    # and we want to save results in two separate folders. 
    # It can be done like this:

    $ psd2bandpwr ~/pipeline/*subj_id_Control* 8 12 -d ~/Controls_alpha
    
    $ psd2bandpwr ~/pipeline/*subj_id_Patient* 8 12 -d ~/Patients_alpha