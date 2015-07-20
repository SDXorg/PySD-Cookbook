
Parallel Model Fitting
======================

.. code:: python

    %pylab inline
    import pandas as pd
    import pysd
    import scipy.optimize


.. parsed-literal::

    Populating the interactive namespace from numpy and matplotlib


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



.. code:: python

    data.shape




.. parsed-literal::

    (3137, 20)



.. code:: python

    model = pysd.read_vensim('../../models/Aging_Chain/Aging_Chain.mdl')

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

.. code:: python

    import datetime
    print datetime.datetime.now()
    county_params = data.apply(fit, axis=1)
    print datetime.datetime.now()


.. parsed-literal::

    2015-07-14 13:54:45.516392
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    2015-07-14 14:30:27.537515


.. code:: python

    county_params.plot(kind='hist', bins=100, alpha=.1, histtype='stepfilled')
    plt.xlim(-.)




.. parsed-literal::

    <matplotlib.axes._subplots.AxesSubplot at 0x1213e2310>




.. image:: Massively%20Parallel%20Fitting_files/Massively%20Parallel%20Fitting_7_1.png


.. code:: python

    df2 = county_params.drop('dec_1_loss_rate',1)

.. code:: python

    import numpy as np
    import seaborn

.. code:: python

    df2.plot(kind='hist', bins=np.arange(-.15,.4,.01), alpha=.4, histtype='stepfilled')
    plt.xlim(-.15,.4)
    plt.title('Fit yearly loss rates from each US county\n by age bracket from 2000 to 2010', fontsize=16)
    plt.ylabel('Number of Counties', fontsize=16)
    plt.xlabel('Yearly Loss Rate in 1% Brackets', fontsize=16)
    plt.legend(frameon=False, fontsize=14)
    plt.savefig('Loss_Histogram.svg')



.. image:: Massively%20Parallel%20Fitting_files/Massively%20Parallel%20Fitting_10_0.png


.. code:: python

    plt.savefig('Loss_Histogram.pdf')



.. parsed-literal::

    <matplotlib.figure.Figure at 0x10d122e10>


This snippet comes from https://gist.github.com/yong27/7869662

.. code:: python

    %%capture
    
    import multiprocessing
    
    def _apply_df(args):
        df, func, kwargs = args
        return df.apply(func, **kwargs)
    
    def apply_by_multiprocessing(df, func, workers, **kwargs):
        pool = multiprocessing.Pool(processes=workers)
        result = pool.map(_apply_df, [(d, func, kwargs) for d in np.array_split(df, workers)])
        pool.close()
        return pd.concat(list(result))
    
    county_params = apply_by_multiprocessing(data[:10], fit, axis=1, workers=4)
    



.. parsed-literal::

    2015-07-17 12:54:25.153590
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    
    Excess work done on this call (perhaps wrong Dfun type).Excess work done on this call (perhaps wrong Dfun type).Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    
    
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    
    Excess work done on this call (perhaps wrong Dfun type).Excess work done on this call (perhaps wrong Dfun type).Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    
    
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    
    
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    
    Run with full_output = 1 to get quantitative information.
    
    Excess work done on this call (perhaps wrong Dfun type).Excess work done on this call (perhaps wrong Dfun type).Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    
    
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    
    
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    
    
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    
    Excess work done on this call (perhaps wrong Dfun type).Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).Excess work done on this call (perhaps wrong Dfun type).Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    
    
    
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    
    Excess work done on this call (perhaps wrong Dfun type).Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    
    2015-07-17 12:54:29.525746
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    
    Excess work done on this call (perhaps wrong Dfun type).Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    
    
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    
    Excess work done on this call (perhaps wrong Dfun type).
    
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    
    Excess work done on this call (perhaps wrong Dfun type).Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    
    
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    
    Excess work done on this call (perhaps wrong Dfun type).
    
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Run with full_output = 1 to get quantitative information.
    Excess work done on this call (perhaps wrong Dfun type).
    Run with full_output = 1 to get quantitative information.


