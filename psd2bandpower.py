import click
import numpy as np
import os
import re

def get_band_power(psds, freqs, band):
    assert np.all(np.mean(psds) < 1E6), "We need the raw psds, not the psds converted to dB."
    bands = [(0, 4, 'Delta'),
             (4, 8, 'Theta'),
             (8, 12, 'Alpha'),
             (12, 30, 'Beta'),
             (30, 100, 'Gamma')]

    data = np.empty(shape=(psds.shape[0], len(bands)), dtype=np.float32)


    for i, (fmin, fmax, title) in enumerate(bands):
        freq_mask = (fmin <= freqs) & (freqs < fmax)
        if freq_mask.sum() == 0:
            raise RuntimeError('No frequencies in band "{name}" ({fmin}, {fmax}).\nFreqs:\n{freqs}'.format(
                name=title, fmin=fmin, fmax=fmax, freqs=freqs))

        data[:, i] = np.mean(psds[:, freq_mask], axis=1)

    data = 10 * np.log10(data)

    return data


def get_psds_and_freqs_from_dir(dirname):
    is_found_psds = False
    is_found_freqs = False

    for fname in os.listdir(dirname):

        if not is_found_psds:
            match_psds  = re.search(r'(.*)psds\.npy', fname)
            if match_psds:
                psds_fname = os.path.join(dirname, match_psds.group(0))
                psds_basename = match_psds.group(1)

                psds = np.load(psds_fname)
                is_found_psds = True

        if not is_found_freqs:
            match_freqs = re.search(r'(.*)freqs\.npy', fname)
            if match_freqs:
                freqs_fname = os.path.join(dirname, match_freqs.group(0))
                freqs_basename = match_freqs.group(1)
                freqs = np.load(freqs_fname)
                is_found_freqs = True

    if not is_found_psds:
        raise RuntimeError('No -psds.npy file in {dirname}'.format(dirname=dirname))
    if not is_found_freqs:
        raise RuntimeError('No -freqs.npy file in {dirname}'.format(dirname=dirname))

    if psds_basename == freqs_basename:
        return psds, freqs
    else:
        raise RuntimeError('Different basenames for  "{psds_fnmame}" and "{freqs_fname}" '.format(psds_fname=psds_fname, freqs_fname=freqs_fname))


@click.command()
@click.argument('pwr_dirs', nargs=-1)
def cli(pwr_dirs):
    """
    Find [basename]-psds.npy and [basename]-freqs.npy in pwr_dirs, load them to compute power in a band and save the result
    N.B.: Each dir must contain only one instance of [basename]-psds.npy and [basename]-freqs.npy 
    """
    for pwr_dir in pwr_dirs:
        try: 
            psds, freqs = get_psds_and_freqs_from_dir(pwr_dir)
        except:
            click.echo('Failed for {}'.format(pwr_dir))


#

