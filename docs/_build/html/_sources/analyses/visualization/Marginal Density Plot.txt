
Demo of a KDE plot beside timeseries set
========================================

.. code:: python

    %pylab inline
    import pysd
    import numpy as np
    import pandas as pd
    import seaborn


.. parsed-literal::

    Populating the interactive namespace from numpy and matplotlib


Load the model using PySD
~~~~~~~~~~~~~~~~~~~~~~~~~

The model is a basic, 1-stock carbon bathtub model

.. code:: python

    model = pysd.read_vensim('../../models/Climate/Atmospheric_Bathtub.mdl')
    print model.doc()


.. parsed-literal::

    |    | name                      | modelName                 | unit        | comment                                    |
    |----+---------------------------+---------------------------+-------------+--------------------------------------------|
    |  0 | Emissions                 | emissions                 |             | nan                                        |
    |  1 | Excess Atmospheric Carbon | excess_atmospheric_carbon |             | nan                                        |
    |  2 | FINAL TIME                | final_time                | Month       | The final time for the simulation.         |
    |  3 | INITIAL TIME              | initial_time              | Month       | The initial time for the simulation.       |
    |  4 | Natural Removal           | natural_removal           |             | nan                                        |
    |  5 | Removal Constant          | removal_constant          |             | nan                                        |
    |  6 | SAVEPER                   | saveper                   | Month [0,?] | The frequency with which output is stored. |
    |  7 | TIME STEP                 | time_step                 | Month [0,?] | The time step for the simulation.          |


Generate a set of parameters to use as input
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here, drawing 1000 constant values for the ``Emissions`` parameter from
an exponential distribution

.. code:: python

    n_runs = 1000
    runs = pd.DataFrame({'Emissions': np.random.exponential(scale=10000, size=n_runs)})
    runs.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Emissions</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>754.742333</td>
        </tr>
        <tr>
          <th>1</th>
          <td>14749.039754</td>
        </tr>
        <tr>
          <th>2</th>
          <td>7241.957594</td>
        </tr>
        <tr>
          <th>3</th>
          <td>4284.263487</td>
        </tr>
        <tr>
          <th>4</th>
          <td>22376.864579</td>
        </tr>
      </tbody>
    </table>
    </div>



Run the model with the various parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    result = runs.apply(lambda p: model.run(params=dict(p))['Excess Atmospheric Carbon'],
                        axis=1).T
    result.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>0</th>
          <th>1</th>
          <th>2</th>
          <th>3</th>
          <th>4</th>
          <th>5</th>
          <th>6</th>
          <th>7</th>
          <th>8</th>
          <th>9</th>
          <th>...</th>
          <th>990</th>
          <th>991</th>
          <th>992</th>
          <th>993</th>
          <th>994</th>
          <th>995</th>
          <th>996</th>
          <th>997</th>
          <th>998</th>
          <th>999</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0.0</th>
          <td>0.000000</td>
          <td>0.000000</td>
          <td>0.000000</td>
          <td>0.000000</td>
          <td>0.000000</td>
          <td>0.000000</td>
          <td>0.000000</td>
          <td>0.000000</td>
          <td>0.000000</td>
          <td>0.000000</td>
          <td>...</td>
          <td>0.000000</td>
          <td>0.000000</td>
          <td>0.000000</td>
          <td>0.000000</td>
          <td>0.000000</td>
          <td>0.000000</td>
          <td>0.000000</td>
          <td>0.000000</td>
          <td>0.000000</td>
          <td>0.000000</td>
        </tr>
        <tr>
          <th>1.0</th>
          <td>754.742333</td>
          <td>14749.039754</td>
          <td>7241.957594</td>
          <td>4284.263487</td>
          <td>22376.864579</td>
          <td>8302.073685</td>
          <td>23364.988335</td>
          <td>9642.752933</td>
          <td>9246.002982</td>
          <td>29150.232322</td>
          <td>...</td>
          <td>6422.187598</td>
          <td>10433.929055</td>
          <td>5228.257878</td>
          <td>29585.251330</td>
          <td>7903.097871</td>
          <td>7765.682923</td>
          <td>5425.788505</td>
          <td>8576.242429</td>
          <td>18934.396132</td>
          <td>3688.825398</td>
        </tr>
        <tr>
          <th>2.0</th>
          <td>1501.937242</td>
          <td>29350.589111</td>
          <td>14411.495612</td>
          <td>8525.684340</td>
          <td>44529.960511</td>
          <td>16521.126633</td>
          <td>46496.326786</td>
          <td>19189.078336</td>
          <td>18399.545933</td>
          <td>58008.962321</td>
          <td>...</td>
          <td>12780.153321</td>
          <td>20763.518819</td>
          <td>10404.233177</td>
          <td>58874.650147</td>
          <td>15727.164763</td>
          <td>15453.709018</td>
          <td>10797.319125</td>
          <td>17066.722433</td>
          <td>37679.448302</td>
          <td>7340.762543</td>
        </tr>
        <tr>
          <th>3.0</th>
          <td>2241.660202</td>
          <td>43806.122973</td>
          <td>21509.338250</td>
          <td>12724.690984</td>
          <td>66461.525485</td>
          <td>24657.989052</td>
          <td>69396.351853</td>
          <td>28639.940486</td>
          <td>27461.553456</td>
          <td>86579.105020</td>
          <td>...</td>
          <td>19074.539386</td>
          <td>30989.812686</td>
          <td>15528.448722</td>
          <td>87871.154975</td>
          <td>23472.990987</td>
          <td>23064.854851</td>
          <td>16115.134440</td>
          <td>25472.297638</td>
          <td>56237.049950</td>
          <td>10956.180316</td>
        </tr>
        <tr>
          <th>4.0</th>
          <td>2973.985933</td>
          <td>58117.101498</td>
          <td>28536.202462</td>
          <td>16881.707561</td>
          <td>88173.774809</td>
          <td>32713.482847</td>
          <td>92067.376669</td>
          <td>37996.294014</td>
          <td>36432.940903</td>
          <td>114863.546291</td>
          <td>...</td>
          <td>25305.981590</td>
          <td>41113.843614</td>
          <td>20601.422113</td>
          <td>116577.694755</td>
          <td>31141.358948</td>
          <td>30599.889226</td>
          <td>21379.771600</td>
          <td>33793.817090</td>
          <td>74609.075583</td>
          <td>14535.443911</td>
        </tr>
      </tbody>
    </table>
    <p>5 rows × 1000 columns</p>
    </div>



Draw a plot showing the results, and a marginal density plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    # left side should have all traces plotted
    plt.subplot2grid((1,4), loc=(0,0), colspan=3)
    [plt.plot(result.index, result[i], 'b', alpha=.02) for i in result.columns]
    plt.ylim(0, max(result.iloc[-1]))
    
    # right side has gaussian KDE on last timestamp
    plt.subplot2grid((1,4), loc=(0,3))
    seaborn.kdeplot(result.iloc[-1], vertical=True)
    plt.ylim(0, max(result.iloc[-1]));
    plt.yticks([])
    plt.xticks([])
    
    plt.suptitle('Emissions scenarios under uncertainty', fontsize=16);



.. image:: Marginal%20Density%20Plot_files/Marginal%20Density%20Plot_9_0.png

