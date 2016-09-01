import click
import numpy as np
import os
import re


def get_band_power(psds, freqs, band):
    """
    Compute power in frequency band. Works both with 2-d and 3-d psds tensors.
    """
    assert np.all(np.mean(psds) <
                  1E6), "We need the raw psds, not the psds converted to dB."
    data = np.empty(shape=psds.shape[:-1], dtype=np.float32)

    freq_mask = (band[0] <= freqs) & (freqs < band[1])
    if freq_mask.sum() == 0:
        raise RuntimeError('No frequencies in band ({fmin}, {fmax}).\nFreqs:\n{freqs}'.format(
            fmin=band[0], fmax=band[1], freqs=freqs))
    # "..." is to address both 2-d and 3-d cases.
    data = np.mean(psds[..., freq_mask], axis=psds.ndim -
                   1) * (band[1] - band[0])
    # data = 10 * np.log10(data)

    return data


def get_psds_and_freqs_from_dir(dirname):
    is_found_psds = False
    is_found_freqs = False

    for fname in os.listdir(dirname):

        if not is_found_psds:
            match_psds = re.search(r'(.*)psds\.npy', fname)
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
        raise RuntimeError(
            'No -psds.npy file in {dirname}'.format(dirname=dirname))
    if not is_found_freqs:
        raise RuntimeError(
            'No -freqs.npy file in {dirname}'.format(dirname=dirname))

    if psds_basename == freqs_basename:
        return psds, freqs, psds_basename
    else:
        raise RuntimeError('Different basenames for  "{psds_fnmame}" and "{freqs_fname}" '.format(
            psds_fname=psds_fname, freqs_fname=freqs_fname))


def band_str(band):
    if int(band[0]) == band[0]:
        fmin = int(band[0])
    else:
        fmin = band[0]

    if int(band[1]) == band[1]:
        fmax = int(band[1])
    else:
        fmax = band[1]

    return str(fmin) + '_' + str(fmax)


@click.command()
@click.argument('pwr_dirs', nargs=-1, type=click.Path(exists=True))
@click.argument('band', nargs=2, type=float)
@click.option('-n', '--bandname', type=unicode, help='Name of band added to filename at saving')
@click.option('-d', '--destdir', type=click.Path(), help='Destination directory; if unset, save to the same direcotory where loaded psds and freqs from')
def cli(pwr_dirs, band, bandname, destdir):
    """
    Find [basename]-psds.npy and [basename]-freqs.npy in [PWR_DIRS], load them to compute power in a BAND and save the result to [basename][-bandname][_band]-pwr.npy

    Each dir must contain only one instance of [basename]-psds.npy and [basename]-freqs.npy 

    EXAMPLES:

        Say, we have a pipeline folder with psds computed. Each subfolder has psds and freqs files inside. The most basic usage would be

        $ psd2bandpwr ~/pipeline/*subj_id* 8 12 


        This will compute power in alpha band for each subject in ~/pipeline



        Now assume we have two groups: controls and patients and we want to save results in two separate folders. It can be done like this:

        $ psd2bandpwr ~/pipeline/*subj_id_Control* 8 12 -d ~/Controls_alpha


        $ psd2bandpwr ~/pipeline/*subj_id_Patient* 8 12 -d ~/Patients_alpha

    """
    for pwr_dir in pwr_dirs:
        try:
            psds, freqs, basename = get_psds_and_freqs_from_dir(pwr_dir)
        except:
            click.echo('Error: Loading psds failed for {}'.format(pwr_dir))
            continue
        # print pwr_dir
        data = get_band_power(psds, freqs, band)
        if destdir:
            savedir = destdir
            if not os.path.isdir(destdir):
                os.makedirs(destdir)
        else:
            savedir = pwr_dir

        save_fname = os.path.join(savedir, basename)
        if bandname:
            save_fname = save_fname + bandname + '_'

        save_fname = save_fname + band_str(band) + '-pwr.npy'
        np.save(save_fname, data)
