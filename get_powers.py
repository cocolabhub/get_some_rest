import click
import pickle as pkl
import pandas as pd
import numpy as np
from os.path import abspath
import re

from psd2bandpower import get_band_power


@click.command()
@click.argument('npy_files', nargs=-1)
@click.option('--savename', '-s', type=click.Path())
@click.option('--band', '-b', nargs=2, type=click.Tuple([float, float]), multiple=True)
@click.option('--debug/--no-debug', default=False)
def cli(npy_files, savename, band, debug):
    """Prepare dataframe with power spectral densities"""
    subj_names, conds, labels = [], [], []
    npy_files = [abspath(f) for f in npy_files]
    n_bands = len(band)
    subj_band_powers = [None] * n_bands
    band_powers = []

    for npy_file in npy_files:
        if debug: click.echo(npy_file)

        psd_freqs = np.load(npy_file)

        # psds.append(psd_freqs['psds'])
        # freqs.append(psd_freqs['freqs'])
        for i, b in enumerate(band):
            subj_band_powers[i] = get_band_power(psd_freqs['psds'], psd_freqs['freqs'], b)
            # if debug: print(subj_band_powers)
        band_powers.append(subj_band_powers[:])

        sID, label = extract_sID(npy_file, debug)
        subj_names.append(sID)
        labels.append(label)

        cond = extract_cond(npy_file, debug)
        conds.append(cond)


    df_dict = {'fname': npy_files, 'subj_name': subj_names, 'label': labels, 'condition': conds}
    for i, b in enumerate(band):
        b_str = '{} {}'.format(b[0], b[1]) 
        bp = [band_powers[j][i] for j in range(len(band_powers))]
        if debug: print(bp.shape)
        df_dict[b_str] = bp

    df = pd.DataFrame(data=df_dict)
    if debug:
        click.echo(df)
    df.to_pickle(savename)


def extract_sID(npy_path, debug):
    ''' Extract subject name from a path '''
    match_sID = re.search(r'.*_((K|R)[0-9]{4})_.*', npy_path)
    if match_sID:
        sID = match_sID.group(1)
        group = match_sID.group(2)
        if debug:
            click.echo(sID)
            click.echo(group)
        if group == 'K':
            label = 1
        elif group == 'R':
            label = 0
        return sID, label


def extract_cond(npy_path, debug):
    ''' Extract condition name from a path '''
    match_cond = re.search(r'.*(eo|ec)-.*', npy_path)
    if match_cond:
        cond = match_cond.group(1)
        if debug:
            click.echo(cond)
        return(cond)
