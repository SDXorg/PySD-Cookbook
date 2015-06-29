
Ebola Data Loader
=================

In this notebook, we'll format data from `The World Health
Organization <http://apps.who.int/gho/data/view.ebola-sitrep.ebola-country-SLE-20150422-graph?lang=en>`__
for future analysis

.. code:: python

    %pylab inline
    import pandas as pd
    import re


.. parsed-literal::

    Populating the interactive namespace from numpy and matplotlib


.. code:: python

    #read in the raw data
    rawdata = pd.read_csv('Ebola_in_SL_Raw_WHO_Data.csv')
    rawdata.iloc[1]




.. parsed-literal::

    COUNTRY (CODE)                                     SLE
    COUNTRY (DISPLAY)                         Sierra Leone
    COUNTRY (URL)                                      NaN
    EBOLA_MEASURE (CODE)                             CASES
    EBOLA_MEASURE (DISPLAY)                Number of cases
    EBOLA_MEASURE (URL)                                NaN
    CASE_DEFINITION (CODE)                       CONFIRMED
    CASE_DEFINITION (DISPLAY)                    Confirmed
    CASE_DEFINITION (URL)                              NaN
    EBOLA_DATA_SOURCE (CODE)                     PATIENTDB
    EBOLA_DATA_SOURCE (DISPLAY)           Patient database
    EBOLA_DATA_SOURCE (URL)                            NaN
    EPI_WEEK (CODE)                               2015-W07
    EPI_WEEK (DISPLAY)              09 to 15 February 2015
    EPI_WEEK (URL)                                     NaN
    INDICATOR_TYPE (CODE)                       SITREP_NEW
    INDICATOR_TYPE (DISPLAY)                           New
    INDICATOR_TYPE (URL)                               NaN
    DATAPACKAGEID (CODE)                        2015-04-22
    DATAPACKAGEID (DISPLAY)        Data package 2015-04-22
    DATAPACKAGEID (URL)                                NaN
    Display Value                                       92
    Numeric                                             92
    Low                                                NaN
    High                                               NaN
    Comments                                           NaN
    Name: 1, dtype: object



.. code:: python

    #parse the dates column
    import dateutil
    
    def parsedate(week_string):
        end_date_str = re.split(' to ', week_string)[1]
        return(dateutil.parser.parse(end_date_str))
    
    rawdata['End Date'] = rawdata['EPI_WEEK (DISPLAY)'].apply(parsedate)
    rawdata.head()




.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>COUNTRY (CODE)</th>
          <th>COUNTRY (DISPLAY)</th>
          <th>COUNTRY (URL)</th>
          <th>EBOLA_MEASURE (CODE)</th>
          <th>EBOLA_MEASURE (DISPLAY)</th>
          <th>EBOLA_MEASURE (URL)</th>
          <th>CASE_DEFINITION (CODE)</th>
          <th>CASE_DEFINITION (DISPLAY)</th>
          <th>CASE_DEFINITION (URL)</th>
          <th>EBOLA_DATA_SOURCE (CODE)</th>
          <th>...</th>
          <th>INDICATOR_TYPE (URL)</th>
          <th>DATAPACKAGEID (CODE)</th>
          <th>DATAPACKAGEID (DISPLAY)</th>
          <th>DATAPACKAGEID (URL)</th>
          <th>Display Value</th>
          <th>Numeric</th>
          <th>Low</th>
          <th>High</th>
          <th>Comments</th>
          <th>End Date</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>SLE</td>
          <td>Sierra Leone</td>
          <td>NaN</td>
          <td>CASES</td>
          <td>Number of cases</td>
          <td>NaN</td>
          <td>CONFIRMED</td>
          <td>Confirmed</td>
          <td>NaN</td>
          <td>SITREP</td>
          <td>...</td>
          <td>NaN</td>
          <td>2015-04-22</td>
          <td>Data package 2015-04-22</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>2014-02-23</td>
        </tr>
        <tr>
          <th>1</th>
          <td>SLE</td>
          <td>Sierra Leone</td>
          <td>NaN</td>
          <td>CASES</td>
          <td>Number of cases</td>
          <td>NaN</td>
          <td>CONFIRMED</td>
          <td>Confirmed</td>
          <td>NaN</td>
          <td>PATIENTDB</td>
          <td>...</td>
          <td>NaN</td>
          <td>2015-04-22</td>
          <td>Data package 2015-04-22</td>
          <td>NaN</td>
          <td>92</td>
          <td>92</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>2015-02-15</td>
        </tr>
        <tr>
          <th>2</th>
          <td>SLE</td>
          <td>Sierra Leone</td>
          <td>NaN</td>
          <td>CASES</td>
          <td>Number of cases</td>
          <td>NaN</td>
          <td>CONFIRMED</td>
          <td>Confirmed</td>
          <td>NaN</td>
          <td>PATIENTDB</td>
          <td>...</td>
          <td>NaN</td>
          <td>2015-04-22</td>
          <td>Data package 2015-04-22</td>
          <td>NaN</td>
          <td>455</td>
          <td>455</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>2014-10-19</td>
        </tr>
        <tr>
          <th>3</th>
          <td>SLE</td>
          <td>Sierra Leone</td>
          <td>NaN</td>
          <td>CASES</td>
          <td>Number of cases</td>
          <td>NaN</td>
          <td>CONFIRMED</td>
          <td>Confirmed</td>
          <td>NaN</td>
          <td>SITREP</td>
          <td>...</td>
          <td>NaN</td>
          <td>2015-04-22</td>
          <td>Data package 2015-04-22</td>
          <td>NaN</td>
          <td>63</td>
          <td>63</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>2015-02-22</td>
        </tr>
        <tr>
          <th>4</th>
          <td>SLE</td>
          <td>Sierra Leone</td>
          <td>NaN</td>
          <td>CASES</td>
          <td>Number of cases</td>
          <td>NaN</td>
          <td>CONFIRMED</td>
          <td>Confirmed</td>
          <td>NaN</td>
          <td>SITREP</td>
          <td>...</td>
          <td>NaN</td>
          <td>2015-04-22</td>
          <td>Data package 2015-04-22</td>
          <td>NaN</td>
          <td>80</td>
          <td>80</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>2015-02-01</td>
        </tr>
      </tbody>
    </table>
    <p>5 rows × 27 columns</p>
    </div>



.. code:: python

    data = rawdata[rawdata['EBOLA_DATA_SOURCE (CODE)']=='PATIENTDB']
    data = data[['End Date','Numeric']]
    data.sort(columns='End Date', inplace=True)
    data.dropna(inplace=True)
    data['Timedelta'] = data['End Date']-data['End Date'].iloc[0]
    data['Weeks'] = data['Timedelta'].apply(lambda a: pd.tslib.Timedelta(a).days/7)
    data.set_index('Weeks', inplace=True)
    data = data[['Numeric']]
    data.columns=['New Reported Cases']
    data['Cumulative Cases'] = data['New Reported Cases'].cumsum()

.. code:: python

    data.plot()




.. parsed-literal::

    <matplotlib.axes._subplots.AxesSubplot at 0x10bb9a990>




.. image:: Ebola_Data_Loader_files/Ebola_Data_Loader_5_1.png


.. code:: python

    data.to_csv('Ebola_in_SL_Data.csv')

