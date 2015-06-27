
Baby Name Data
==============

This notebook formats data from the social security administration `baby
names database <http://www.ssa.gov/oact/babynames/limits.html>`__ into a
format that is easy for the cookbook to deal with. It expects the zip
file to be unpacked into a subfolder called 'names'.

.. code:: python

    import pandas as pd
    import glob

.. code:: python

    filenames = glob.glob('names/yob*')

.. code:: python

    females = pd.DataFrame()
    males = pd.DataFrame()
    
    for filename in filenames:
        year = filename[9:13]
        data = pd.read_csv(filename, header=None, names=['Name','Gender',year], index_col='Name')
        females = females.join(data[data['Gender']=='F'].drop('Gender', axis=1), how='outer')
        males = males.join(data[data['Gender']=='M'].drop('Gender', axis=1), how='outer')
    
    females.to_csv('female_names_timeseries.csv')
    males.to_csv('male_names_timeseries.csv')
