import click
# from mne import read_ctf
import contextlib
import sys
from mne import find_layout
from  os.path import commonprefix as cprfx
from os.path import split, splitext, exists, join
from os import makedirs
from mne.io import Raw as Raw_fif
from mne.io import read_raw_ctf as Raw_ctf
from scipy.io import savemat


@contextlib.contextmanager
def nostdout():
    # -- Works both in python2 and python3 -- #
    try:
        from cStringIO import StringIO
    except ImportError:
        from io import StringIO
    # --------------------------------------- #
    save_stdout = sys.stdout 
    sys.stdout = StringIO()
    yield
    sys.stdout = save_stdout


@click.command()
@click.argument('save_path', type=click.Path())
@click.argument('meg_files', nargs=-1)
@click.option('--flat/--no-flat', default=False)
def cli(meg_files, save_path, flat):
    '''Convert fif or ds to .mat format'''
    common_prefix = split(cprfx(meg_files))[0] + '/'
    for meg_file in meg_files:
        # click.echo(meg_file)
        base, ext = splitext(meg_file)
        new_base = base.replace(common_prefix, '')

        if flat:
            new_base = new_base.replace('/','_')

        # click.echo(new_base)
        new_base = join(save_path, new_base) 

        if ext == '.fif':
            with nostdout(): 
                raw = Raw_fif(meg_file, preload=True, add_eeg_ref=False)
        elif ext == '.ds':
            with nostdout(): 
                raw = Raw_ctf(meg_file, preload=True, add_eeg_ref=False)
        else:
            click.echo('ERROR: UNKNOWN FORMAT FOR {}'.format(meg_file)) 

        meg_raw = raw.pick_types(meg=True)
        data, times = meg_raw[:,:]
        ch_names = meg_raw.info['ch_names']
        pos = find_layout(meg_raw.info).pos[:,:2]
        # click.echo(pos)
        new_path,_ = split(new_base) 

        if not exists(new_path):
            makedirs(new_path)

        savemat(new_base + '.mat', {'data': data, 'times': times, 'chnames': ch_names, 'chxy': pos})