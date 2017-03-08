
Plotting a Suite of Simulations
===============================

When we run a suite of simulations, such as when performing sensitivity
tests or uncertainty propagation, it can be handy to plot that suite of
runs together, and give the viewer a sense for how the uncertainty is
manifest over the course of the simulation.

Libraries
~~~~~~~~~

In addition to the standard plotting, simulation and data handling
libraries, we'll use the ``seaborn`` plotting library to handle density
plots.

.. code:: python

    %pylab inline
    import pysd
    import numpy as np
    import pandas as pd
    import seaborn


.. parsed-literal::

    Populating the interactive namespace from numpy and matplotlib


.. parsed-literal::

    /Users/houghton/anaconda/lib/python2.7/site-packages/matplotlib/__init__.py:872: UserWarning: axes.color_cycle is deprecated and replaced with axes.prop_cycle; please use the latter.
      warnings.warn(self.msg_depr % (key, alt_key))


Loading Model
~~~~~~~~~~~~~

The model we'll use in this example is a basic, 1-stock carbon bathtub
model, in which ``Emissions`` contribute to a stock of
``Excess Atmospheric Carbon``, which is slowly depleted through a
process of ``Natural Removal``. |Atmospheric Bathtub|.

.. |Atmospheric Bathtub| image:: ../../models/Climate/Atmospheric_Bathtub.png

.. code:: python

    model = pysd.read_vensim('../../models/Climate/Atmospheric_Bathtub.mdl')

Creating a suite of run parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We'll generate a suite of simulations by drawing 1000 constant values
for the ``Emissions`` parameter from an exponential distribution.

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
          <td>30098.171119</td>
        </tr>
        <tr>
          <th>1</th>
          <td>7539.944593</td>
        </tr>
        <tr>
          <th>2</th>
          <td>621.230074</td>
        </tr>
        <tr>
          <th>3</th>
          <td>677.414622</td>
        </tr>
        <tr>
          <th>4</th>
          <td>2150.153371</td>
        </tr>
      </tbody>
    </table>
    </div>



Run the model with the various parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Next we'll run the model with our various values for emissions, and
collect the resulting timeseries values of the stock of
``Excess Atmospheric Carbon``.

The resulting dataframe ``result`` contains a column for each value
simulation run, and these will form the traces for our plot.

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
          <td>30098.171119</td>
          <td>7539.944593</td>
          <td>621.230074</td>
          <td>677.414622</td>
          <td>2150.153371</td>
          <td>22998.607950</td>
          <td>8930.516487</td>
          <td>14811.709610</td>
          <td>18992.458123</td>
          <td>5168.853388</td>
          <td>...</td>
          <td>11691.074339</td>
          <td>7156.798755</td>
          <td>7650.493678</td>
          <td>45222.958816</td>
          <td>4855.876077</td>
          <td>607.567918</td>
          <td>17004.674837</td>
          <td>4598.519574</td>
          <td>622.265199</td>
          <td>530.692727</td>
        </tr>
        <tr>
          <th>2.0</th>
          <td>59895.360527</td>
          <td>15004.489740</td>
          <td>1236.247847</td>
          <td>1348.055098</td>
          <td>4278.805208</td>
          <td>45767.229820</td>
          <td>17771.727808</td>
          <td>29475.302124</td>
          <td>37794.991665</td>
          <td>10286.018242</td>
          <td>...</td>
          <td>23265.237935</td>
          <td>14242.029522</td>
          <td>15224.482419</td>
          <td>89993.688043</td>
          <td>9663.193393</td>
          <td>1209.060157</td>
          <td>33839.302926</td>
          <td>9151.053953</td>
          <td>1238.307746</td>
          <td>1056.078527</td>
        </tr>
        <tr>
          <th>3.0</th>
          <td>89394.578041</td>
          <td>22394.389436</td>
          <td>1845.115443</td>
          <td>2011.989170</td>
          <td>6386.170526</td>
          <td>68308.165472</td>
          <td>26524.527017</td>
          <td>43992.258713</td>
          <td>56409.499872</td>
          <td>15352.011448</td>
          <td>...</td>
          <td>34723.659895</td>
          <td>21256.407982</td>
          <td>22722.731273</td>
          <td>134316.709979</td>
          <td>14422.437536</td>
          <td>1804.537474</td>
          <td>50505.584734</td>
          <td>13658.062988</td>
          <td>1848.189868</td>
          <td>1576.210468</td>
        </tr>
        <tr>
          <th>4.0</th>
          <td>118598.803380</td>
          <td>29710.390134</td>
          <td>2447.894362</td>
          <td>2669.283900</td>
          <td>8472.462192</td>
          <td>90623.691767</td>
          <td>35189.798234</td>
          <td>58364.045736</td>
          <td>74837.862997</td>
          <td>20367.344722</td>
          <td>...</td>
          <td>46067.497636</td>
          <td>28200.642656</td>
          <td>30145.997638</td>
          <td>178196.501695</td>
          <td>19134.089238</td>
          <td>2394.060017</td>
          <td>67005.203723</td>
          <td>18120.001933</td>
          <td>2451.973168</td>
          <td>2091.141091</td>
        </tr>
      </tbody>
    </table>
    <p>5 rows × 1000 columns</p>
    </div>



Draw a static plot showing the results, and a marginal density plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The code below is what we might use for making a static graphic for
publication in a print environment. The result is an image, and we have
programmatic control over how we want the image displayed and saved.

In the lefthand side of the plot, we draw all traces from the suite of
simulation runs. Plotting each line in the same color, and setting a low
value for ``alpha``, the opacity of each line, we can see the regions of
the plot in which a large number of simulations agree on the values the
system will take, despite the parametric uncertainty.

In the righthand plot, we use a gaussian `Kernel Density Estimator <>`__
provided by the `seaborn <>`__ library. The KDE gives an indication of
the regions in which the density of simulation results is highest, at a
specific time point in the simulation, which we refer to here as
``density_time``.

To indicate the simulation time for which we are displaying a density
estimate, we'll add a vertical line at the point on the lefthand plot at
which the density curve is calculated.

.. code:: python

    # define when to show the density
    density_time = 85
    
    # left side: plot all traces, slightly transparent
    plt.subplot2grid((1,4), loc=(0,0), colspan=3)
    [plt.plot(result.index, result[i], 'b', alpha=.02) for i in result.columns]
    ymax = result.max().max()
    plt.ylim(0, ymax)
    
    # left side: add marker of density location
    plt.vlines(density_time, 0, ymax, 'k')
    plt.text(density_time, ymax, 'Density Calculation', ha='right', va='top', rotation=90)
    
    # right side: gaussian KDE on selected timestamp
    plt.subplot2grid((1,4), loc=(0,3))
    seaborn.kdeplot(result.loc[density_time], vertical=True)
    plt.ylim(0, ymax)
    plt.yticks([])
    plt.xticks([])
    plt.xlabel('Density')
    
    plt.suptitle('Emissions scenarios under uncertainty', fontsize=16);



.. image:: plotting_suite_of_simulations_files/plotting_suite_of_simulations_10_0.png


Static density plot with selector
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For purposes of lightweight exploration, we can add a slider to the
chart. In this case, whenever the slider is moved, the figure is
regenerated, making this a suitable method for exploring results before
feeding in to print graphics.

.. code:: python

    import matplotlib as mpl
    from ipywidgets import interact, IntSlider
    sim_time = 200
    slider_time = IntSlider(description = 'Select Time for plotting Density',
                            min=0, max=result.index[-1], value=1)

.. code:: python

    @interact(density_time=slider_time)
    def update(density_time): 
        ax1 = plt.subplot2grid((1,4), loc=(0,0), colspan=3)
        [ax1.plot(result.index, result[i], 'b', alpha=.02) for i in result.columns]
        ymax = result.max().max()
        ax1.set_ylim(0, ymax)
    
        # left side: add marker of density location
        ax1.vlines(density_time, 0, ymax, 'k')
        ax1.text(density_time, ymax, 'Density Calculation', ha='right', va='top', rotation=90)
    
        # right side: gaussian KDE on selected timestamp
        ax2 = plt.subplot2grid((1,4), loc=(0,3))
        seaborn.kdeplot(result.loc[density_time], vertical=True, ax=ax2)
        ax2.set_ylim(0, ymax)
        ax2.set_yticks([])
        ax2.set_xticks([])
        ax2.set_xlabel('Density')
    
        plt.suptitle('Emissions scenarios under uncertainty', fontsize=16);
        



.. image:: plotting_suite_of_simulations_files/plotting_suite_of_simulations_13_0.png

