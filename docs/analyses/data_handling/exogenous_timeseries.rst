
Exogenous model input from a file
=================================

In this notebook we'll demonstrate using an external data source to feed
values into a model. We'll use the carbon emissions dataset, and feed
total emissions into a stock of excess atmospheric carbon:

We'll begin as usual by importing PySD and the machinery we need in
order to deal with data manipulation and plotting.

.. code:: python

    %pylab inline
    import pysd
    import pandas as pd


.. parsed-literal::

    Populating the interactive namespace from numpy and matplotlib


.. parsed-literal::

    /Users/houghton/anaconda/lib/python2.7/site-packages/pandas/computation/__init__.py:19: UserWarning: The installed version of numexpr 2.4.4 is not supported in pandas and will be not be used
    
      UserWarning)


We use `Pandas <>`__ library to import emissions data from a ``.csv``
file. In this command, we both rename the columns of the dataset, and
set the index to the 'Year' column.

.. code:: python

    emissions = pd.read_csv('../../data/Climate/global_emissions.csv', 
                            skiprows=2, index_col='Year',
                            names=['Year', 'Total Emissions', 
                                   'Gas Emissions', 'Liquid Emissions', 
                                   'Solid Emissions', 'Cement Emissions', 
                                   'Flare Emissions', 'Per Capita Emissions'])
    emissions.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Total Emissions</th>
          <th>Gas Emissions</th>
          <th>Liquid Emissions</th>
          <th>Solid Emissions</th>
          <th>Cement Emissions</th>
          <th>Flare Emissions</th>
          <th>Per Capita Emissions</th>
        </tr>
        <tr>
          <th>Year</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>1751</th>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>1752</th>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>1753</th>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>1754</th>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>1755</th>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>NaN</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    model = pysd.read_vensim('../../models/Climate/Atmospheric_Bathtub.mdl')

In our vensim model file, the value of the inflow to the carbon bathtub,
the ``Emissions`` parameter, is set to zero. We want to instead have
this track our exogenous data.

.. code:: python

    Emissions=
        0

    Excess Atmospheric Carbon= INTEG (
        Emissions - Natural Removal,
        0)

    Natural Removal=
        Excess Atmospheric Carbon * Removal Constant

    Removal Constant=
        0.01

Aligning the model time bounds with that of the dataset
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before we can substitute in our exogenous data, however, we need to
ensure that the model will execute over the proper timeseries. The
initial and final times of the simulation are specified in the model
file as:

.. code:: python

    print 'initial:', model.components.initial_time() 
    print 'final:', model.components.final_time()


.. parsed-literal::

    initial: 0
    final: 100


However, the time frame of the dataset runs:

.. code:: python

    print 'initial:', emissions.index[0]
    print 'final:', emissions.index[-1] 


.. parsed-literal::

    initial: 1751
    final: 2011


In order to run the model over a time series equal to that of the data
set, we need to specify the appropriate initial conditions, and ask the
run function to return to us timestamps equal to that of our dataset:

.. code:: python

    res = model.run(initial_condition=(emissions.index[0], 
                                       {'Excess Atmospheric Carbon': 0}),
                    return_timestamps=emissions.index.values,
                    return_columns=['Emissions', 'Excess Atmospheric Carbon'])
    res.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Emissions</th>
          <th>Excess Atmospheric Carbon</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>1751</th>
          <td>0</td>
          <td>0.0</td>
        </tr>
        <tr>
          <th>1752</th>
          <td>0</td>
          <td>0.0</td>
        </tr>
        <tr>
          <th>1753</th>
          <td>0</td>
          <td>0.0</td>
        </tr>
        <tr>
          <th>1754</th>
          <td>0</td>
          <td>0.0</td>
        </tr>
        <tr>
          <th>1755</th>
          <td>0</td>
          <td>0.0</td>
        </tr>
      </tbody>
    </table>
    </div>



Pass in our timeseries data
~~~~~~~~~~~~~~~~~~~~~~~~~~~

In place of the constant value of ``emissions``, we want to substitute
our dataset. We can do this in a very straightforward way by passing the
Pandas ``Series`` corresponding to the dataset in a dictionary to the
``params`` argument of the run function.

.. code:: python

    res = model.run(initial_condition=(emissions.index[0], 
                                       {'Excess Atmospheric Carbon': 0}),
                    return_timestamps=emissions.index.values,
                    return_columns=['Emissions', 'Excess Atmospheric Carbon'],
                    params={'Emissions': emissions['Total Emissions']})

.. code:: python

    res.plot();



.. image:: exogenous_timeseries_files/exogenous_timeseries_15_0.png


