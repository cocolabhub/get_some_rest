from setuptools import setup

setup(
    name='get_some_rest',
    version='0.1',
    py_modules=['ica_var', 'bst2mne'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        ica_var=ica_var:cli
        bst2mne=bst2mne:cli
    ''',
)