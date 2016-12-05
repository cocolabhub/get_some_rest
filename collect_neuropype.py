"""Command line interface tool to collect output from neuropype"""

import click
import os
import re
import glob



@click.group(chain=True)
@click.option('--workflow', '-w', type=click.Path())
@click.option('--subj-id-regexp', '-r', type=click.STRING)
def cli(workflow, subj_id_regexp):
    """Collect data from neuropype in pandas dataframe"""
    output_greeting()
    

@cli.resultcallback()
def create_dataframe(plchldr, workflow, subj_id_regexp):
    
    click.echo(os.listdir(workflow))
    files = [os.path.join(workflow, f) for f in os.listdir(workflow)]

    for f in filter(os.path.isdir,  files):
        f = os.path.abspath(f)
        print(f)
        sID, label = extract_sID(f, r'.*_((K|R)[0-9]{4})_.*', False)
        print(sID)
    pass




@cli.command('pwr')
def pwr():
    import time
    time_range = range(100)
    with click.progressbar(time_range, fill_char=click.style('>', fg='cyan'), color='cyan') as bar:
        for timelapse in bar:
            time.sleep(0.01)
    pass


def extract_sID(npy_path, regex_str, debug):
    """Extract subject name from a path"""
    match_sID = re.search(regex_str, npy_path)
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

def output_greeting():
    """Produce greeting ascii"""
    click.echo(click.style(r'''
                                   _.-'-'--._
                                  ,', ~'` ( .'`.
                                 ( ~'_ , .'(  >-)
           _ _           _      ( .-' (  `__.-<  )
  ___ ___ | | | ___  ___| |_     ( `-..--'_   .-')
 / __/ _ \| | |/ _ \/ __| __|     `(_( (-' `-'.-)
| (_| (_) | | |  __/ (__| |_          `-.__.-'=/
 \___\___/|_|_|\___|\___|\__|            `._`='
                                            \\
                                                   
 _ __   ___ _   _ _ __ ___  _ __  _   _ _ __   ___ 
| '_ \ / _ \ | | | '__/ _ \| '_ \| | | | '_ \ / _ \
| | | |  __/ |_| | | | (_) | |_) | |_| | |_) |  __/
|_| |_|\___|\__,_|_|  \___/| .__/ \__, | .__/ \___|
                           |_|    |___/|_|         
''', fg='magenta'))


