import click
from mne.preprocessing import read_ica
import contextlib
import sys
import cStringIO

@contextlib.contextmanager
def nostdout():
    save_stdout = sys.stdout
    sys.stdout = cStringIO.StringIO()
    yield
    sys.stdout = save_stdout


@click.command()
@click.argument('subjdirs', nargs=-1)
def cli(subjdirs):
    """
    Convert brainstorm epochs to mne.Epochs object
    """
    for fname in subjdirs:
        with nostdout():
            ica = read_ica(fname)
        n_comp = ica.n_components_
        tot_var = ica.pca_explained_variance_.sum()
        n_comp_var = ica.pca_explained_variance_[:n_comp].sum()
        PVE = n_comp_var / tot_var
        click.echo(PVE)
