import click
import pickle as pkl
import pandas as pd
import numpy as np



@click.command()
@click.argument('pickle_file', type=click.Path())
@click.option('--table', '-t', type=click.Path(), multiple=True)
def cli(pickle_file, table):
    df = pd.read_pickle(pickle_file)
    age_column = 'Age relatively KABC, in month'
    sLength = len(df['subj_name'])
    df['age'] = np.nan
    # print(df)
    for t in table:
        sheet = pd.read_csv(t)
        for name in sheet['ID']:
            if name in df['subj_name'].values:
                
                age = sheet[sheet['ID'] == name][age_column].values[0]

                df.loc[df['subj_name'] == name, 'age'] = age
            else:
                print('Skipping: {}'.format(name))
    # print(df)
    df.to_pickle(pickle_file)
