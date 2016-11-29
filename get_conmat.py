import click
from os.path import abspath
import numpy as np
import pandas as pd
import re

@click.command()
@click.argument('npy_files', nargs=-1)
@click.option('--savename', '-s', type=click.Path())
@click.option('--debug/--no-debug', default=False)
def cli(npy_files, savename, debug):
    ''' Prepare connectivity matrices for machine learning'''
    conmats, subj_names, conds, fbands, labels = [], [], [], [], []
    npy_files = [abspath(f) for f in npy_files]

    for npy_file in npy_files:
        if debug: click.echo(npy_file)

        conmat = np.load(npy_file)
        conmats.append(conmat)
        sID, label = extract_sID(npy_file, debug)
        subj_names.append(sID)
        labels.append(label)
        conds.append(extract_cond(npy_file, debug))
        fbands.append(extract_band(npy_file, debug))
        

    df_dict = {'fname': npy_files, 'con_matrix': conmats, 'subj_name': subj_names, 'label': labels, 'condition': conds, 'freq_band': fbands}
    df = pd.DataFrame(data=df_dict)
    if debug:
        click.echo(df)
    df.to_pickle(savename)


    if debug: click.echo(conmat.shape)

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

def extract_band(npy_path, debug):
    ''' Extract frequency band from a path '''
    match_fband = re.search(r'.*_([0-9]+\.[0-9]+)\.([0-9]+\.[0-9]+)/.*', npy_path)
    if match_fband:
        l_band = float(match_fband.group(1)) 
        h_band = float(match_fband.group(2))
        if debug:
            click.echo('l_band = {}, h_band = {}'.format(l_band, h_band))
        return l_band, h_band

