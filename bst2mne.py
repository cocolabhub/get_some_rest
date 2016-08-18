import click
from mne.preprocessing import read_ica
import contextlib
import sys
import cStringIO
import scipy.io as sio
import numpy as np
from mne import create_info, EpochsArray
from mne.io.pick import channel_type


@contextlib.contextmanager
def nostdout():
    save_stdout = sys.stdout
    sys.stdout = cStringIO.StringIO()
    yield
    sys.stdout = save_stdout


@click.command()
@click.argument('matfiles', nargs=-1)
@click.option('--savename', '-s', default='foo-epo.fif')
@click.option('--rec-type', type=click.Choice(['ds', 'fif']), default='ds')
@click.option('--infosrc', '-i', help='file to take info from')
def cli(matfiles, savename, rec_type, infosrc):
    """
    Convert brainstorm epochs to mne.Epochs object
    """
    if infosrc:
        if rec_type is 'ds':
            from mne.io import read_raw_ctf as read_raw
        elif rec_type is 'fif':
            from mne.io import Raw as read_raw
        with nostdout():
            raw_with_info = read_raw(infosrc)

    isFirst = True
    for fname in matfiles:
        with nostdout():
            mat_epoch = sio.loadmat(fname)
            # click.echo(mat_epoch)
        if isFirst:
            data = mat_epoch['F']
            times = mat_epoch['Time']
            # print times[0,-1]
            isFirst = False
        else:
            data = np.dstack((data, mat_epoch['F']))
        # click.echo(data.shape)
    data = data.transpose((2,0,1))


    n_channels = data.shape[1]
    sfreq = times.shape[1] / (times[0,-1] + times[0,1])
    
    
    if infosrc:
        if rec_type is 'ds':
            from mne.io import read_raw_ctf as read_raw
        elif rec_type is 'fif':
            from mne.io import Raw as read_raw

        with nostdout():
            raw_with_info = read_raw(infosrc)
        good_info = raw_with_info.info
        # click.echo(len(good_info['ch_names']))

        ch_types = [channel_type(good_info, idx) for idx in range(n_channels)]

        # click.echo(len(ch_types))

        info = create_info(ch_names=good_info['ch_names'], sfreq=sfreq, ch_types=ch_types)
    else:
        ch_types='mag'
        info = create_info(n_channels, sfreq, ch_types)

    with nostdout():
        epochs = EpochsArray(data, info)
    epochs.save(savename)