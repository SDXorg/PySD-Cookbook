
Parallel Model Fitting
======================

In this notebook, we'll fit a simple ageing model to all of the counties
in the United States. As before, we'll use ``scipy.optimize`` to perform
the fitting, but we'll use python's ``multiprocessing`` library to
perform these optimizations in parallel.

When to use this technique
--------------------------

This technique is appropriate when we are modeling a large number of
entirely independent but structurally identical systems. In this
example, we're conceptualizing the population of counties to be
influenced by aging and exogenous migration patterns. If we were to
attempt to link the models together, for instance by specifying that the
outmigration from one county needed to be accounted for as the
inmigration to another county, we would need to perform a single
large-scale optimization, or some form of hybrid.

.. code:: python

    %pylab inline
    import pandas as pd
    import pysd
    import scipy.optimize
    import multiprocessing
    import numpy as np
    import seaborn


.. parsed-literal::

    Populating the interactive namespace from numpy and matplotlib


Ingredients
-----------

Data
^^^^

The first ingredient theat we'll use is census data from the 2000 and
2010 census:

.. code:: python

    data = pd.read_csv('../../data/Census/Males by decade and county.csv', header=[0,1], skiprows=[2])
    data.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr>
          <th></th>
          <th>Unnamed: 0_level_0</th>
          <th>Unnamed: 1_level_0</th>
          <th colspan="9" halign="left">2000</th>
          <th colspan="9" halign="left">2010</th>
        </tr>
        <tr>
          <th></th>
          <th>Unnamed: 0_level_1</th>
          <th>Unnamed: 1_level_1</th>
          <th>dec_1</th>
          <th>dec_2</th>
          <th>dec_3</th>
          <th>dec_4</th>
          <th>dec_5</th>
          <th>dec_6</th>
          <th>dec_7</th>
          <th>dec_8</th>
          <th>dec_9</th>
          <th>dec_1</th>
          <th>dec_2</th>
          <th>dec_3</th>
          <th>dec_4</th>
          <th>dec_5</th>
          <th>dec_6</th>
          <th>dec_7</th>
          <th>dec_8</th>
          <th>dec_9</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>1</td>
          <td>1</td>
          <td>3375</td>
          <td>3630</td>
          <td>2461</td>
          <td>3407</td>
          <td>3283</td>
          <td>2319</td>
          <td>1637</td>
          <td>825</td>
          <td>284</td>
          <td>3867</td>
          <td>4384</td>
          <td>3082</td>
          <td>3598</td>
          <td>4148</td>
          <td>3390</td>
          <td>2293</td>
          <td>1353</td>
          <td>454</td>
        </tr>
        <tr>
          <th>1</th>
          <td>1</td>
          <td>3</td>
          <td>9323</td>
          <td>10094</td>
          <td>7600</td>
          <td>9725</td>
          <td>10379</td>
          <td>8519</td>
          <td>6675</td>
          <td>4711</td>
          <td>1822</td>
          <td>11446</td>
          <td>12006</td>
          <td>9976</td>
          <td>11042</td>
          <td>12517</td>
          <td>12368</td>
          <td>10623</td>
          <td>6307</td>
          <td>2911</td>
        </tr>
        <tr>
          <th>2</th>
          <td>1</td>
          <td>5</td>
          <td>2002</td>
          <td>2198</td>
          <td>2412</td>
          <td>2465</td>
          <td>2178</td>
          <td>1699</td>
          <td>1026</td>
          <td>689</td>
          <td>301</td>
          <td>1673</td>
          <td>1739</td>
          <td>2260</td>
          <td>2208</td>
          <td>2233</td>
          <td>1910</td>
          <td>1490</td>
          <td>739</td>
          <td>324</td>
        </tr>
        <tr>
          <th>3</th>
          <td>1</td>
          <td>7</td>
          <td>1546</td>
          <td>1460</td>
          <td>1680</td>
          <td>1762</td>
          <td>1624</td>
          <td>1237</td>
          <td>774</td>
          <td>475</td>
          <td>187</td>
          <td>1471</td>
          <td>1577</td>
          <td>1798</td>
          <td>2016</td>
          <td>1928</td>
          <td>1581</td>
          <td>1140</td>
          <td>579</td>
          <td>211</td>
        </tr>
        <tr>
          <th>4</th>
          <td>1</td>
          <td>9</td>
          <td>3741</td>
          <td>3615</td>
          <td>3393</td>
          <td>3901</td>
          <td>3773</td>
          <td>3007</td>
          <td>2227</td>
          <td>1269</td>
          <td>550</td>
          <td>3741</td>
          <td>4252</td>
          <td>3312</td>
          <td>3719</td>
          <td>4129</td>
          <td>3782</td>
          <td>3052</td>
          <td>1723</td>
          <td>652</td>
        </tr>
      </tbody>
    </table>
    </div>



Model
^^^^^

The model will be a simple ageing chain that groups individuals into 10
year cohorts.

.. code:: python

    model = pysd.read_vensim('../../models/Aging_Chain/Aging_Chain.mdl')

The Recipe
----------

As in our other optimization problems, we'll construct an error function
that calculates the sum of squared errors between our model prediction
and the measured data. We also construct a helper function called
``fit`` which basically makes the call to the optimizer and formats the
result in something that we can aggregate into a Pandas DataFrame.

.. code:: python

    param_names = ['dec_%i_loss_rate'%i for i in range(1,10)]
    
    def error(param_vals, measurements):
        predictions = model.run(params=dict(zip(param_names, param_vals)),
                                initial_condition=(2000,measurements['2000']),
                                return_timestamps=2010,
                                rtol=1).loc[2010]
    
        errors = predictions - measurements['2010']
        return sum(errors.values[1:]**2) #ignore first decade: no birth info
    
    def fit(row):
        res = scipy.optimize.minimize(error, args=row,
                                      x0=[.05]*9,
                                      method='L-BFGS-B');
        return pd.Series(index=['dec_%i_loss_rate'%i for i in range(1,10)], data=res['x'])

At this point, fitting the model is a simple matter of applying the fit
function to the data:

.. code:: python

    %%capture
    county_params = data.apply(fit, axis=1)

On my 2014 era machine, this optimization takes about half an hour.

We can plot the distributions of the fit parameters for each of the
counties in a histogram, to get a sense of the result. (Here we're
ignoring the first decade, which will not have reasonable parameters, as
we have no information about births to the system.)

.. code:: python

    df2 = county_params.drop('dec_1_loss_rate',1)
    df2.plot(kind='hist', bins=np.arange(-.15,.4,.01), alpha=.4, histtype='stepfilled')
    plt.xlim(-.15,.4)
    plt.title('Fit yearly loss rates from each US county\n by age bracket from 2000 to 2010', fontsize=16)
    plt.ylabel('Number of Counties', fontsize=16)
    plt.xlabel('Yearly Loss Rate in 1% Brackets', fontsize=16)
    plt.legend(frameon=False, fontsize=14)
    plt.savefig('Loss_Histogram.svg')



.. image:: Massively_Parallel_Fitting_files/Massively_Parallel_Fitting_11_0.png


Executing the optimization in parallel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We can take advantage of the multicore nature of most modern machines by
using python's ``multiprocessing`` module to distribute the various
counties between each of the cores we have available for the
calculation. The basic structure for this piece of code comes from `this
gist <https://gist.github.com/yong27/7869662>`__. We are essentially
creating a helper function that will apply the fit function to a subset
of the census DataFrame, and calling this function once on each of our
worker nodes.

.. code:: python

    %%capture
    
    def _apply_df(args):
        df, func, kwargs = args
        return df.apply(func, **kwargs)
    
    def apply_by_multiprocessing(df, func, workers, **kwargs):
        pool = multiprocessing.Pool(processes=workers)
        result = pool.map(_apply_df, [(d, func, kwargs) for d in np.array_split(df, workers)])
        pool.close()
        return pd.concat(list(result))
    
    county_params = apply_by_multiprocessing(data[:10], fit, axis=1, workers=4)
