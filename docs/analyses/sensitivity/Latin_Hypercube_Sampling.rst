
.. code:: python

    %matplotlib inline
    import pysd
    import numpy as np
    import pandas as pd
    import pyDOE
    import scipy.stats.distributions as dist
    import multiprocessing


.. parsed-literal::

    /Users/houghton/anaconda/lib/python2.7/site-packages/pandas/computation/__init__.py:19: UserWarning: The installed version of numexpr 2.4.4 is not supported in pandas and will be not be used
    
      UserWarning)


.. code:: python

    model = pysd.read_vensim('../../models/Capability_Trap/Capability Trap.mdl')

.. code:: python

    # define the sample space
    ranges = {'Fraction of Effort for Sales':(0,1),
              'Startup Subsidy':(0,2),
              'Startup Subsidy Length':(0,12)}
    
    # generate LHS samples within the unit square
    lhs = pyDOE.lhs(n=len(ranges), samples=2000)
    
    # transform samples into our sample space
    samples = pd.DataFrame(
        data=dist.uniform(loc=[x[0] for x in ranges.values()],
                          scale=[x[1] for x in ranges.values()]).ppf(lhs),
        columns=ranges.keys())
    
    samples.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Capability</th>
          <th>Pressure to Do Work</th>
          <th>Pressure to Improve Capability</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0.0000</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>0.0625</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>0.1250</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>0.1875</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>0.2500</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>0.3125</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>0.3750</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>0.4375</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>0.5000</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>0.5625</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>0.6250</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>0.6875</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>0.7500</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>0.8125</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>0.8750</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>0.9375</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>1.0000</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>1.0625</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>1.1250</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>1.1875</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>1.2500</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>1.3125</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>1.3750</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>1.4375</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>1.5000</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>1.5625</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>1.6250</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>1.6875</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>1.7500</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>1.8125</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>...</th>
          <td>...</td>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th>98.1875</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>98.2500</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>98.3125</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>98.3750</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>98.4375</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>98.5000</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>98.5625</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>98.6250</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>98.6875</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>98.7500</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>98.8125</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>98.8750</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>98.9375</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>99.0000</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>99.0625</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>99.1250</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>99.1875</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>99.2500</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>99.3125</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>99.3750</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>99.4375</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>99.5000</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>99.5625</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>99.6250</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>99.6875</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>99.7500</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>99.8125</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>99.8750</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>99.9375</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
        <tr>
          <th>100.0000</th>
          <td>100.0</td>
          <td>1.0</td>
          <td>1.0</td>
        </tr>
      </tbody>
    </table>
    <p>1601 rows × 3 columns</p>
    </div>



.. code:: python

    def runner(params):
        market = market_model.run(dict(params),return_columns=['Tenure'])
        motiv = motivation_model.run(dict(params),return_columns=['Tenure'])
        return pd.Series({'market':market['Tenure'].iloc[-1], 
                          'motivation':motiv['Tenure'].iloc[-1]})

.. code:: python

    def _apply_df(args):
        df, func, kwargs = args
        return df.apply(func, **kwargs)
    
    def apply_by_multiprocessing(df, func, workers=multiprocessing.cpu_count(), **kwargs):
        pool = multiprocessing.Pool(processes=workers)
        result = pool.map(_apply_df, [(d, func, kwargs) for d in np.array_split(df, workers)])
        pool.close()
        return pd.concat(list(result))
    
    res = apply_by_multiprocessing(samples, runner, axis=1)

.. code:: python

    # define the sample space
    ranges = {'Fraction of Effort for Sales':(0,1),
              'Startup Subsidy':(0,2),
              'Startup Subsidy Length':(0,12)}
    
    # generate LHS samples within the unit square
    lhs = pyDOE.lhs(n=len(ranges), samples=2000)
    
    # transform samples into our sample space
    samples = pd.DataFrame(
        data=dist.uniform(loc=[x[0] for x in ranges.values()],
                          scale=[x[1] for x in ranges.values()]).ppf(lhs),
        columns=ranges.keys())
    
    samples.head()
