
Demo of a KDE plot beside timeseries set
========================================

.. code:: python

    %pylab inline
    #%matplotlib inline
    #import matplotlib.pyplot as plt
    import mpld3
    #mpld3.enable_notebook()
    #%matplotlib notebook
    #
    import pysd
    import numpy as np
    import pandas as pd
    import seaborn


.. parsed-literal::

    Populating the interactive namespace from numpy and matplotlib


::


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-1-aa729ffbe7f3> in <module>()
          6 #%matplotlib notebook
          7 #
    ----> 8 import pysd
          9 import numpy as np
         10 import pandas as pd


    /Users/houghton/Google_Drive/Academic Projects/PYSD/pysd/pysd/__init__.py in <module>()
          1 from .pysd import read_vensim, load, PySD
    ----> 2 from . import functions
          3 from . import utils
          4 from ._version import __version__
          5 


    /Users/houghton/Google_Drive/Academic Projects/PYSD/pysd/pysd/functions.py in <module>()
        270         return expr
        271 
    --> 272 class Delay(object):
        273     def __init__(self, order, init=0):
        274         self.chain = np.ndarray()


    /Users/houghton/Google_Drive/Academic Projects/PYSD/pysd/pysd/functions.py in Delay()
        278 
        279 
    --> 280     state
        281 
        282 delay123 = Delay(3)


    NameError: name 'state' is not defined


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
          <td>2862.573249</td>
        </tr>
        <tr>
          <th>1</th>
          <td>23208.933671</td>
        </tr>
        <tr>
          <th>2</th>
          <td>30256.409702</td>
        </tr>
        <tr>
          <th>3</th>
          <td>10339.757007</td>
        </tr>
        <tr>
          <th>4</th>
          <td>2843.203204</td>
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
          <td>2862.573249</td>
          <td>23208.933671</td>
          <td>30256.409702</td>
          <td>10339.757007</td>
          <td>2843.203204</td>
          <td>5347.545999</td>
          <td>47284.180637</td>
          <td>10923.619315</td>
          <td>5636.865090</td>
          <td>22313.016387</td>
          <td>...</td>
          <td>4371.735736</td>
          <td>7190.321753</td>
          <td>1640.460139</td>
          <td>19084.475809</td>
          <td>6220.337224</td>
          <td>7377.659406</td>
          <td>770.703843</td>
          <td>18197.870295</td>
          <td>17326.924760</td>
          <td>4827.955762</td>
        </tr>
        <tr>
          <th>2.0</th>
          <td>5696.520766</td>
          <td>46185.778005</td>
          <td>60210.255307</td>
          <td>20576.116444</td>
          <td>5657.974376</td>
          <td>10641.616537</td>
          <td>94095.519468</td>
          <td>21738.002436</td>
          <td>11217.361530</td>
          <td>44402.902611</td>
          <td>...</td>
          <td>8699.754114</td>
          <td>14308.740289</td>
          <td>3264.515676</td>
          <td>37978.106859</td>
          <td>12378.471076</td>
          <td>14681.542218</td>
          <td>1533.700647</td>
          <td>36213.761886</td>
          <td>34480.580271</td>
          <td>9607.631966</td>
        </tr>
        <tr>
          <th>3.0</th>
          <td>8502.128807</td>
          <td>68932.853896</td>
          <td>89864.562456</td>
          <td>30710.112286</td>
          <td>8444.597837</td>
          <td>15882.746370</td>
          <td>140438.744910</td>
          <td>32444.241727</td>
          <td>16742.053004</td>
          <td>66271.889972</td>
          <td>...</td>
          <td>12984.492309</td>
          <td>21355.974640</td>
          <td>4872.330659</td>
          <td>56682.801600</td>
          <td>18475.023589</td>
          <td>21912.386202</td>
          <td>2289.067483</td>
          <td>54049.494562</td>
          <td>51462.699228</td>
          <td>14339.511408</td>
        </tr>
        <tr>
          <th>4.0</th>
          <td>11279.680768</td>
          <td>91452.459027</td>
          <td>119222.326534</td>
          <td>40742.768171</td>
          <td>11203.355062</td>
          <td>21071.464905</td>
          <td>186318.538098</td>
          <td>43043.418625</td>
          <td>22211.497565</td>
          <td>87922.187460</td>
          <td>...</td>
          <td>17226.383122</td>
          <td>28332.736647</td>
          <td>6464.067491</td>
          <td>75200.449392</td>
          <td>24510.610577</td>
          <td>29070.921746</td>
          <td>3036.880651</td>
          <td>71706.869911</td>
          <td>68274.996996</td>
          <td>19024.072056</td>
        </tr>
      </tbody>
    </table>
    <p>5 rows × 1000 columns</p>
    </div>



Draw a static plot showing the results, and a marginal density plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This would be for making graphics for a publication, where you don't
want an interactive view, but you want fine control over what the figure
looks like.

This is relatively simple, because we rely on the plotting library
``seaborn`` to generate the KDE plot, instead of working out the
densities ourselves.

.. code:: python

    import matplotlib.pylab as plt
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



.. image:: Marginal%20Density%20Plot%20-%20Interactive_files/Marginal%20Density%20Plot%20-%20Interactive_9_0.png


Interactive plot using python backend
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following would be for lightweight exploration

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
        



.. image:: Marginal%20Density%20Plot%20-%20Interactive_files/Marginal%20Density%20Plot%20-%20Interactive_12_0.png


Interactive figure with javascript background
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This script would prepare interactive graphics to share on a webpage,
independent of the python backend.


.. code:: python

    import mpld3

.. code:: python

    from mpld3 import plugins
    
    fig, ax = plt.subplots(3, 3, figsize=(6, 6))
    fig.subplots_adjust(hspace=0.1, wspace=0.1)
    ax = ax[::-1]
    
    X = np.random.normal(size=(3, 100))
    for i in range(3):
        for j in range(3):
            ax[i, j].xaxis.set_major_formatter(plt.NullFormatter())
            ax[i, j].yaxis.set_major_formatter(plt.NullFormatter())
            points = ax[i, j].scatter(X[j], X[i])
            
    plugins.connect(fig, plugins.LinkedBrush(points))


.. parsed-literal::

    /Users/houghton/anaconda/lib/python2.7/site-packages/IPython/core/formatters.py:92: DeprecationWarning: DisplayFormatter._ipython_display_formatter_default is deprecated: use @default decorator instead.
      def _ipython_display_formatter_default(self):
    /Users/houghton/anaconda/lib/python2.7/site-packages/IPython/core/formatters.py:669: DeprecationWarning: PlainTextFormatter._singleton_printers_default is deprecated: use @default decorator instead.
      def _singleton_printers_default(self):



.. raw:: html

    
    
    <style>
    
    </style>
    
    <div id="fig_el9000145509147684824814976"></div>
    <script>
    function mpld3_load_lib(url, callback){
      var s = document.createElement('script');
      s.src = url;
      s.async = true;
      s.onreadystatechange = s.onload = callback;
      s.onerror = function(){console.warn("failed to load library " + url);};
      document.getElementsByTagName("head")[0].appendChild(s);
    }
    
    if(typeof(mpld3) !== "undefined" && mpld3._mpld3IsLoaded){
       // already loaded: just create the figure
       !function(mpld3){
           
           mpld3.draw_figure("fig_el9000145509147684824814976", {"axes": [{"xlim": [-3.0, 3.0], "yscale": "linear", "axesbg": "#EAEAF2", "texts": [], "zoomable": true, "images": [], "xdomain": [-3.0, 3.0], "ylim": [-3.0, 3.0], "paths": [], "sharey": [], "sharex": [], "axesbgalpha": null, "axes": [{"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "bottom", "nticks": 7, "tickvalues": null}, {"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "left", "nticks": 7, "tickvalues": null}], "lines": [], "markers": [], "id": "el900014550916624", "ydomain": [-3.0, 3.0], "collections": [{"paths": [[[[0.0, -0.5], [0.13260155, -0.5], [0.25978993539242673, -0.44731684579412084], [0.3535533905932738, -0.3535533905932738], [0.44731684579412084, -0.25978993539242673], [0.5, -0.13260155], [0.5, 0.0], [0.5, 0.13260155], [0.44731684579412084, 0.25978993539242673], [0.3535533905932738, 0.3535533905932738], [0.25978993539242673, 0.44731684579412084], [0.13260155, 0.5], [0.0, 0.5], [-0.13260155, 0.5], [-0.25978993539242673, 0.44731684579412084], [-0.3535533905932738, 0.3535533905932738], [-0.44731684579412084, 0.25978993539242673], [-0.5, 0.13260155], [-0.5, 0.0], [-0.5, -0.13260155], [-0.44731684579412084, -0.25978993539242673], [-0.3535533905932738, -0.3535533905932738], [-0.25978993539242673, -0.44731684579412084], [-0.13260155, -0.5], [0.0, -0.5]], ["M", "C", "C", "C", "C", "C", "C", "C", "C", "Z"]]], "edgecolors": ["#000000"], "edgewidths": [0.3], "offsets": "data01", "yindex": 1, "id": "el900014599707536", "pathtransforms": [[4.969039949999533, 0.0, 0.0, 4.969039949999533, 0.0, 0.0]], "pathcoordinates": "display", "offsetcoordinates": "data", "zorder": 1, "xindex": 0, "alphas": [null], "facecolors": ["#0000FF"]}], "xscale": "linear", "bbox": [0.125, 0.65781250000000002, 0.2421875, 0.2421875]}, {"xlim": [-4.0, 4.0], "yscale": "linear", "axesbg": "#EAEAF2", "texts": [], "zoomable": true, "images": [], "xdomain": [-4.0, 4.0], "ylim": [-3.0, 3.0], "paths": [], "sharey": [], "sharex": [], "axesbgalpha": null, "axes": [{"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "bottom", "nticks": 9, "tickvalues": null}, {"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "left", "nticks": 7, "tickvalues": null}], "lines": [], "markers": [], "id": "el900014588475472", "ydomain": [-3.0, 3.0], "collections": [{"paths": [[[[0.0, -0.5], [0.13260155, -0.5], [0.25978993539242673, -0.44731684579412084], [0.3535533905932738, -0.3535533905932738], [0.44731684579412084, -0.25978993539242673], [0.5, -0.13260155], [0.5, 0.0], [0.5, 0.13260155], [0.44731684579412084, 0.25978993539242673], [0.3535533905932738, 0.3535533905932738], [0.25978993539242673, 0.44731684579412084], [0.13260155, 0.5], [0.0, 0.5], [-0.13260155, 0.5], [-0.25978993539242673, 0.44731684579412084], [-0.3535533905932738, 0.3535533905932738], [-0.44731684579412084, 0.25978993539242673], [-0.5, 0.13260155], [-0.5, 0.0], [-0.5, -0.13260155], [-0.44731684579412084, -0.25978993539242673], [-0.3535533905932738, -0.3535533905932738], [-0.25978993539242673, -0.44731684579412084], [-0.13260155, -0.5], [0.0, -0.5]], ["M", "C", "C", "C", "C", "C", "C", "C", "C", "Z"]]], "edgecolors": ["#000000"], "edgewidths": [0.3], "offsets": "data01", "yindex": 1, "id": "el900014599709520", "pathtransforms": [[4.969039949999533, 0.0, 0.0, 4.969039949999533, 0.0, 0.0]], "pathcoordinates": "display", "offsetcoordinates": "data", "zorder": 1, "xindex": 2, "alphas": [null], "facecolors": ["#0000FF"]}], "xscale": "linear", "bbox": [0.39140625000000001, 0.65781250000000002, 0.24218749999999994, 0.2421875]}, {"xlim": [-3.0, 3.0], "yscale": "linear", "axesbg": "#EAEAF2", "texts": [], "zoomable": true, "images": [], "xdomain": [-3.0, 3.0], "ylim": [-3.0, 3.0], "paths": [], "sharey": [], "sharex": [], "axesbgalpha": null, "axes": [{"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "bottom", "nticks": 7, "tickvalues": null}, {"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "left", "nticks": 7, "tickvalues": null}], "lines": [], "markers": [], "id": "el900014589019664", "ydomain": [-3.0, 3.0], "collections": [{"paths": [[[[0.0, -0.5], [0.13260155, -0.5], [0.25978993539242673, -0.44731684579412084], [0.3535533905932738, -0.3535533905932738], [0.44731684579412084, -0.25978993539242673], [0.5, -0.13260155], [0.5, 0.0], [0.5, 0.13260155], [0.44731684579412084, 0.25978993539242673], [0.3535533905932738, 0.3535533905932738], [0.25978993539242673, 0.44731684579412084], [0.13260155, 0.5], [0.0, 0.5], [-0.13260155, 0.5], [-0.25978993539242673, 0.44731684579412084], [-0.3535533905932738, 0.3535533905932738], [-0.44731684579412084, 0.25978993539242673], [-0.5, 0.13260155], [-0.5, 0.0], [-0.5, -0.13260155], [-0.44731684579412084, -0.25978993539242673], [-0.3535533905932738, -0.3535533905932738], [-0.25978993539242673, -0.44731684579412084], [-0.13260155, -0.5], [0.0, -0.5]], ["M", "C", "C", "C", "C", "C", "C", "C", "C", "Z"]]], "edgecolors": ["#000000"], "edgewidths": [0.3], "offsets": "data01", "yindex": 1, "id": "el900014594845648", "pathtransforms": [[4.969039949999533, 0.0, 0.0, 4.969039949999533, 0.0, 0.0]], "pathcoordinates": "display", "offsetcoordinates": "data", "zorder": 1, "xindex": 1, "alphas": [null], "facecolors": ["#0000FF"]}], "xscale": "linear", "bbox": [0.65781249999999991, 0.65781250000000002, 0.2421875, 0.2421875]}, {"xlim": [-3.0, 3.0], "yscale": "linear", "axesbg": "#EAEAF2", "texts": [], "zoomable": true, "images": [], "xdomain": [-3.0, 3.0], "ylim": [-4.0, 4.0], "paths": [], "sharey": [], "sharex": [], "axesbgalpha": null, "axes": [{"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "bottom", "nticks": 7, "tickvalues": null}, {"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "left", "nticks": 9, "tickvalues": null}], "lines": [], "markers": [], "id": "el900014590673040", "ydomain": [-4.0, 4.0], "collections": [{"paths": [[[[0.0, -0.5], [0.13260155, -0.5], [0.25978993539242673, -0.44731684579412084], [0.3535533905932738, -0.3535533905932738], [0.44731684579412084, -0.25978993539242673], [0.5, -0.13260155], [0.5, 0.0], [0.5, 0.13260155], [0.44731684579412084, 0.25978993539242673], [0.3535533905932738, 0.3535533905932738], [0.25978993539242673, 0.44731684579412084], [0.13260155, 0.5], [0.0, 0.5], [-0.13260155, 0.5], [-0.25978993539242673, 0.44731684579412084], [-0.3535533905932738, 0.3535533905932738], [-0.44731684579412084, 0.25978993539242673], [-0.5, 0.13260155], [-0.5, 0.0], [-0.5, -0.13260155], [-0.44731684579412084, -0.25978993539242673], [-0.3535533905932738, -0.3535533905932738], [-0.25978993539242673, -0.44731684579412084], [-0.13260155, -0.5], [0.0, -0.5]], ["M", "C", "C", "C", "C", "C", "C", "C", "C", "Z"]]], "edgecolors": ["#000000"], "edgewidths": [0.3], "offsets": "data01", "yindex": 2, "id": "el900014594847632", "pathtransforms": [[4.969039949999533, 0.0, 0.0, 4.969039949999533, 0.0, 0.0]], "pathcoordinates": "display", "offsetcoordinates": "data", "zorder": 1, "xindex": 0, "alphas": [null], "facecolors": ["#0000FF"]}], "xscale": "linear", "bbox": [0.125, 0.39140625000000007, 0.2421875, 0.24218749999999989]}, {"xlim": [-4.0, 4.0], "yscale": "linear", "axesbg": "#EAEAF2", "texts": [], "zoomable": true, "images": [], "xdomain": [-4.0, 4.0], "ylim": [-4.0, 4.0], "paths": [], "sharey": [], "sharex": [], "axesbgalpha": null, "axes": [{"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "bottom", "nticks": 9, "tickvalues": null}, {"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "left", "nticks": 9, "tickvalues": null}], "lines": [], "markers": [], "id": "el900014591252880", "ydomain": [-4.0, 4.0], "collections": [{"paths": [[[[0.0, -0.5], [0.13260155, -0.5], [0.25978993539242673, -0.44731684579412084], [0.3535533905932738, -0.3535533905932738], [0.44731684579412084, -0.25978993539242673], [0.5, -0.13260155], [0.5, 0.0], [0.5, 0.13260155], [0.44731684579412084, 0.25978993539242673], [0.3535533905932738, 0.3535533905932738], [0.25978993539242673, 0.44731684579412084], [0.13260155, 0.5], [0.0, 0.5], [-0.13260155, 0.5], [-0.25978993539242673, 0.44731684579412084], [-0.3535533905932738, 0.3535533905932738], [-0.44731684579412084, 0.25978993539242673], [-0.5, 0.13260155], [-0.5, 0.0], [-0.5, -0.13260155], [-0.44731684579412084, -0.25978993539242673], [-0.3535533905932738, -0.3535533905932738], [-0.25978993539242673, -0.44731684579412084], [-0.13260155, -0.5], [0.0, -0.5]], ["M", "C", "C", "C", "C", "C", "C", "C", "C", "Z"]]], "edgecolors": ["#000000"], "edgewidths": [0.3], "offsets": "data01", "yindex": 2, "id": "el900014599658192", "pathtransforms": [[4.969039949999533, 0.0, 0.0, 4.969039949999533, 0.0, 0.0]], "pathcoordinates": "display", "offsetcoordinates": "data", "zorder": 1, "xindex": 2, "alphas": [null], "facecolors": ["#0000FF"]}], "xscale": "linear", "bbox": [0.39140625000000001, 0.39140625000000007, 0.24218749999999994, 0.24218749999999989]}, {"xlim": [-3.0, 3.0], "yscale": "linear", "axesbg": "#EAEAF2", "texts": [], "zoomable": true, "images": [], "xdomain": [-3.0, 3.0], "ylim": [-4.0, 4.0], "paths": [], "sharey": [], "sharex": [], "axesbgalpha": null, "axes": [{"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "bottom", "nticks": 7, "tickvalues": null}, {"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "left", "nticks": 9, "tickvalues": null}], "lines": [], "markers": [], "id": "el900014591562704", "ydomain": [-4.0, 4.0], "collections": [{"paths": [[[[0.0, -0.5], [0.13260155, -0.5], [0.25978993539242673, -0.44731684579412084], [0.3535533905932738, -0.3535533905932738], [0.44731684579412084, -0.25978993539242673], [0.5, -0.13260155], [0.5, 0.0], [0.5, 0.13260155], [0.44731684579412084, 0.25978993539242673], [0.3535533905932738, 0.3535533905932738], [0.25978993539242673, 0.44731684579412084], [0.13260155, 0.5], [0.0, 0.5], [-0.13260155, 0.5], [-0.25978993539242673, 0.44731684579412084], [-0.3535533905932738, 0.3535533905932738], [-0.44731684579412084, 0.25978993539242673], [-0.5, 0.13260155], [-0.5, 0.0], [-0.5, -0.13260155], [-0.44731684579412084, -0.25978993539242673], [-0.3535533905932738, -0.3535533905932738], [-0.25978993539242673, -0.44731684579412084], [-0.13260155, -0.5], [0.0, -0.5]], ["M", "C", "C", "C", "C", "C", "C", "C", "C", "Z"]]], "edgecolors": ["#000000"], "edgewidths": [0.3], "offsets": "data01", "yindex": 2, "id": "el900014599660368", "pathtransforms": [[4.969039949999533, 0.0, 0.0, 4.969039949999533, 0.0, 0.0]], "pathcoordinates": "display", "offsetcoordinates": "data", "zorder": 1, "xindex": 1, "alphas": [null], "facecolors": ["#0000FF"]}], "xscale": "linear", "bbox": [0.65781249999999991, 0.39140625000000007, 0.2421875, 0.24218749999999989]}, {"xlim": [-3.0, 3.0], "yscale": "linear", "axesbg": "#EAEAF2", "texts": [], "zoomable": true, "images": [], "xdomain": [-3.0, 3.0], "ylim": [-3.0, 3.0], "paths": [], "sharey": [], "sharex": [], "axesbgalpha": null, "axes": [{"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "bottom", "nticks": 7, "tickvalues": null}, {"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "left", "nticks": 7, "tickvalues": null}], "lines": [], "markers": [], "id": "el900014592197968", "ydomain": [-3.0, 3.0], "collections": [{"paths": [[[[0.0, -0.5], [0.13260155, -0.5], [0.25978993539242673, -0.44731684579412084], [0.3535533905932738, -0.3535533905932738], [0.44731684579412084, -0.25978993539242673], [0.5, -0.13260155], [0.5, 0.0], [0.5, 0.13260155], [0.44731684579412084, 0.25978993539242673], [0.3535533905932738, 0.3535533905932738], [0.25978993539242673, 0.44731684579412084], [0.13260155, 0.5], [0.0, 0.5], [-0.13260155, 0.5], [-0.25978993539242673, 0.44731684579412084], [-0.3535533905932738, 0.3535533905932738], [-0.44731684579412084, 0.25978993539242673], [-0.5, 0.13260155], [-0.5, 0.0], [-0.5, -0.13260155], [-0.44731684579412084, -0.25978993539242673], [-0.3535533905932738, -0.3535533905932738], [-0.25978993539242673, -0.44731684579412084], [-0.13260155, -0.5], [0.0, -0.5]], ["M", "C", "C", "C", "C", "C", "C", "C", "C", "Z"]]], "edgecolors": ["#000000"], "edgewidths": [0.3], "offsets": "data01", "yindex": 0, "id": "el900014373148816", "pathtransforms": [[4.969039949999533, 0.0, 0.0, 4.969039949999533, 0.0, 0.0]], "pathcoordinates": "display", "offsetcoordinates": "data", "zorder": 1, "xindex": 0, "alphas": [null], "facecolors": ["#0000FF"]}], "xscale": "linear", "bbox": [0.125, 0.12500000000000011, 0.2421875, 0.2421875]}, {"xlim": [-4.0, 4.0], "yscale": "linear", "axesbg": "#EAEAF2", "texts": [], "zoomable": true, "images": [], "xdomain": [-4.0, 4.0], "ylim": [-3.0, 3.0], "paths": [], "sharey": [], "sharex": [], "axesbgalpha": null, "axes": [{"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "bottom", "nticks": 9, "tickvalues": null}, {"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "left", "nticks": 7, "tickvalues": null}], "lines": [], "markers": [], "id": "el900014592734416", "ydomain": [-3.0, 3.0], "collections": [{"paths": [[[[0.0, -0.5], [0.13260155, -0.5], [0.25978993539242673, -0.44731684579412084], [0.3535533905932738, -0.3535533905932738], [0.44731684579412084, -0.25978993539242673], [0.5, -0.13260155], [0.5, 0.0], [0.5, 0.13260155], [0.44731684579412084, 0.25978993539242673], [0.3535533905932738, 0.3535533905932738], [0.25978993539242673, 0.44731684579412084], [0.13260155, 0.5], [0.0, 0.5], [-0.13260155, 0.5], [-0.25978993539242673, 0.44731684579412084], [-0.3535533905932738, 0.3535533905932738], [-0.44731684579412084, 0.25978993539242673], [-0.5, 0.13260155], [-0.5, 0.0], [-0.5, -0.13260155], [-0.44731684579412084, -0.25978993539242673], [-0.3535533905932738, -0.3535533905932738], [-0.25978993539242673, -0.44731684579412084], [-0.13260155, -0.5], [0.0, -0.5]], ["M", "C", "C", "C", "C", "C", "C", "C", "C", "Z"]]], "edgecolors": ["#000000"], "edgewidths": [0.3], "offsets": "data01", "yindex": 0, "id": "el900014594761552", "pathtransforms": [[4.969039949999533, 0.0, 0.0, 4.969039949999533, 0.0, 0.0]], "pathcoordinates": "display", "offsetcoordinates": "data", "zorder": 1, "xindex": 2, "alphas": [null], "facecolors": ["#0000FF"]}], "xscale": "linear", "bbox": [0.39140625000000001, 0.12500000000000011, 0.24218749999999994, 0.2421875]}, {"xlim": [-3.0, 3.0], "yscale": "linear", "axesbg": "#EAEAF2", "texts": [], "zoomable": true, "images": [], "xdomain": [-3.0, 3.0], "ylim": [-3.0, 3.0], "paths": [], "sharey": [], "sharex": [], "axesbgalpha": null, "axes": [{"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "bottom", "nticks": 7, "tickvalues": null}, {"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "left", "nticks": 7, "tickvalues": null}], "lines": [], "markers": [], "id": "el900014594230032", "ydomain": [-3.0, 3.0], "collections": [{"paths": [[[[0.0, -0.5], [0.13260155, -0.5], [0.25978993539242673, -0.44731684579412084], [0.3535533905932738, -0.3535533905932738], [0.44731684579412084, -0.25978993539242673], [0.5, -0.13260155], [0.5, 0.0], [0.5, 0.13260155], [0.44731684579412084, 0.25978993539242673], [0.3535533905932738, 0.3535533905932738], [0.25978993539242673, 0.44731684579412084], [0.13260155, 0.5], [0.0, 0.5], [-0.13260155, 0.5], [-0.25978993539242673, 0.44731684579412084], [-0.3535533905932738, 0.3535533905932738], [-0.44731684579412084, 0.25978993539242673], [-0.5, 0.13260155], [-0.5, 0.0], [-0.5, -0.13260155], [-0.44731684579412084, -0.25978993539242673], [-0.3535533905932738, -0.3535533905932738], [-0.25978993539242673, -0.44731684579412084], [-0.13260155, -0.5], [0.0, -0.5]], ["M", "C", "C", "C", "C", "C", "C", "C", "C", "Z"]]], "edgecolors": ["#000000"], "edgewidths": [0.3], "offsets": "data01", "yindex": 0, "id": "el900014594845584", "pathtransforms": [[4.969039949999533, 0.0, 0.0, 4.969039949999533, 0.0, 0.0]], "pathcoordinates": "display", "offsetcoordinates": "data", "zorder": 1, "xindex": 1, "alphas": [null], "facecolors": ["#0000FF"]}], "xscale": "linear", "bbox": [0.65781249999999991, 0.12500000000000011, 0.2421875, 0.2421875]}], "height": 480.0, "width": 480.0, "plugins": [{"type": "reset"}, {"enabled": false, "button": true, "type": "zoom"}, {"enabled": false, "button": true, "type": "boxzoom"}, {"enabled": true, "button": true, "type": "linkedbrush", "id": "el900014594845648"}], "data": {"data01": [[0.72627725515196, -0.609617514020416, -0.5085678480094306], [0.45470011425609647, 0.5648926982935867, -0.07229420027544038], [-0.9124990804111092, 0.7810756401052897, 1.2812488443811665], [-0.7158326645558005, 0.25439416295376643, 0.31434136860601114], [-1.3243474989055997, -1.2952343469304026, 0.4754065777451255], [0.20679789169204818, 0.282404609880748, 1.3642822338969176], [-0.4557509822065865, -0.057390405349647504, 0.5354643397144171], [-0.6854256925510113, 1.2669241576729566, -0.481565174156881], [1.814654931930241, 0.18661309228043924, 0.9229610589958064], [0.052483512450695616, 0.3238070594522619, 1.4667236272430229], [0.13314946262202526, 0.32535765075875456, 0.39387343338897307], [0.44802397824046003, -0.3758686066043297, 0.792726218774311], [0.28838791256798113, -2.2127470505539173, 0.5951887985405865], [-0.04808559803838435, -0.012104520906811323, 1.050956950183763], [-0.8470614355031485, -1.1711151292027087, 1.4669946395869475], [0.5368092151501439, -0.7792166458718895, 0.07544892431309147], [1.4161306966828309, -1.7180110153349744, -0.4588268802293387], [-0.9318793884307652, 0.7125841349165489, 0.8655704499664272], [-0.10829885867639287, -0.9008733078048662, -1.3043377768214877], [-2.1120564133627213, -0.16195075185942912, 0.39739069661276416], [2.214811099602801, 0.9768731725614395, -0.6102095163636395], [1.4116382962479617, 1.2360207312265725, -0.9343642775454202], [0.09260686157586422, -1.1632633936028205, -0.2894947669214405], [1.0949929335337916, 0.4185271557657954, -0.8567939512184845], [-1.7348293757022026, -1.4919933255930191, -0.8381261398554098], [-1.1300231659030309, -0.027364650893653423, 0.11456105611135182], [0.04296811728542167, -0.2456817790822539, 0.23363478641727034], [-0.32799259057129415, 0.3451424424062806, 0.5700060750629162], [0.9255284017346328, -0.5670591322601339, 0.7750870513296308], [-0.08832214489077245, 0.29983404037903044, -1.0716826480772965], [-1.638834965530711, -0.38194204616313165, -1.136711044707441], [-0.5575665292820112, -0.08091792457355151, 0.6573602203284092], [0.37365684565744034, 0.3529559632748866, 0.2809258881984997], [0.4887378570322217, 0.1883181271903021, 0.48329021125635835], [0.17081981009178976, -0.3994384119083303, -2.898107886636492], [-0.41481003832437413, -0.15884641897830631, -0.7175629996855155], [0.5340501366272006, -0.32906501874691946, -0.4505594267519602], [-1.021849510491513, 1.1377134720591533, 0.4156376240675203], [-0.15542352142667828, 0.1466651626712377, 1.2817642340791557], [0.784914393549551, 0.0313394406364746, 1.4950548951738316], [-1.5481709714447207, -0.12901799786419965, -0.5330996829018881], [0.4369056050718823, 1.002751646087784, -2.4920690075337713], [1.5701115864102244, -1.6475363688431865, 0.6315677804318997], [1.0554867653362938, -0.2358060348147957, -3.266959888778148], [0.8404585908023985, 1.1581514499158168, 0.1663250543938972], [-0.7845963269487475, 0.33130543902850673, -0.3639803139134531], [0.45996385016833113, 1.4865079106239818, 1.886434068659524], [-0.5976399047987899, -0.4463228319216556, -0.5677397974228435], [-0.3103394440557323, 0.37498315078071864, 1.161281462047915], [1.436493430865783, -0.096681352504951, -1.2382134966592364], [-0.1277445046996717, -0.5040636724904181, -0.9672570417099028], [0.12646602176983848, 0.06999745869739371, 1.5593223284636468], [0.7238563827651077, -0.2582349724261488, 1.0803461260857055], [0.9627315040032325, 0.057620906905957496, 0.06964478084401315], [-0.24632853741784336, -0.3997498441462584, -1.3203974836871593], [-0.7920288712805237, -0.7140809170006572, 0.02088634706964818], [0.1805000557004198, -0.9420378333697007, 0.23586064317623523], [0.554405100440566, -0.28142207029323535, -1.0413287177771662], [0.853192500378185, 0.07035084063503451, 0.4816412277403756], [-0.4122852655096991, -0.6275094466917257, 0.6388292164357494], [-1.7916503324032693, 1.0611842309772412, 0.8043506198561388], [1.499128304380035, -0.22923354435393606, -0.6127739253326915], [0.5877440920038117, -0.09679831519842488, 0.7037686833116943], [0.9312481573556909, 1.2110140339067053, 1.1927568803146646], [0.3004882137247224, 0.20363007936894034, 0.14669002943773124], [-0.7252537272467792, 0.22320786239446536, 0.2687705443151357], [0.008929357633260495, 0.03930191858514528, -1.845114002105977], [0.8346320381668927, -0.3592331298055962, -0.28177403784654914], [-0.2029845612271129, 0.2963894804237323, 1.1564913912014636], [-0.24213933965518933, -1.9853205551530253, 1.1241320679288065], [1.2078111484101128, -0.04451501963175593, -0.33755740650598054], [0.02596642493816797, 0.5896365768471749, 1.7389086851206426], [-0.27272592823462677, -0.34694502323692084, -0.7267491032493013], [0.8705064224086991, 0.46208961203073134, -0.5412201434173727], [0.7858377646861028, 0.023582517005452063, 1.287438045339133], [1.1186765160237864, -1.5721953179179307, 0.89044155895576], [0.848459364855634, -0.0020518836814035343, -0.24644926739502987], [-1.4851792817789338, 0.025858139746513104, -0.009846715062858537], [0.22552813360915355, -0.38899731417893607, 0.2124520593062608], [1.868463602643709, -1.7619530684258848, 0.21475370107315214], [1.0982756880470732, 0.1452010110903084, 0.959355656855051], [0.2469251659721454, -0.29950036079570996, 0.3866760347184457], [0.5550636636168365, -0.07615493442218282, -1.3578999695134073], [-1.1511075167215055, 2.0130702386861214, 1.279947838742059], [-1.230231563968042, 0.5001903412542189, -1.0675891820283898], [-0.48506000456981535, 1.265567266053854, 2.082812115181861], [0.11879725907101205, 0.037140537822488516, -0.3114435839006701], [1.4902779255597118, 2.1297700734265836, 3.400046164356916], [-0.24172607361743356, 0.4004615150134686, -1.242510123566507], [1.6010966219497424, -0.6358910636344438, -0.6031516122144578], [1.386781576515262, -0.48026285883108716, 0.4795284854474212], [2.11299658582516, 0.986205002091192, -0.6816854976351491], [0.7709267112876348, 0.05610026154512464, 0.09272792278109766], [-0.14758532866242421, 1.0385928872415382, -0.46868766931818967], [1.8795447180644578, 0.17071962626703338, 0.012511656685759506], [1.0897120893968824, -0.9756555432684259, -2.429807661934103], [1.5166904646735573, 0.2132197913199486, 0.12465716254859609], [-0.7788432764438152, 1.1472826421052982, -1.0814674209098705], [0.2916684245546782, -0.19838535621231929, -0.7555625626768224], [-0.40415989019521464, 0.6620745944507938, -0.13301100501957958]]}, "id": "el900014550914768"});
       }(mpld3);
    }else if(typeof define === "function" && define.amd){
       // require.js is available: use it to load d3/mpld3
       require.config({paths: {d3: "https://mpld3.github.io/js/d3.v3.min"}});
       require(["d3"], function(d3){
          window.d3 = d3;
          mpld3_load_lib("https://mpld3.github.io/js/mpld3.v0.2.js", function(){
             
             mpld3.draw_figure("fig_el9000145509147684824814976", {"axes": [{"xlim": [-3.0, 3.0], "yscale": "linear", "axesbg": "#EAEAF2", "texts": [], "zoomable": true, "images": [], "xdomain": [-3.0, 3.0], "ylim": [-3.0, 3.0], "paths": [], "sharey": [], "sharex": [], "axesbgalpha": null, "axes": [{"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "bottom", "nticks": 7, "tickvalues": null}, {"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "left", "nticks": 7, "tickvalues": null}], "lines": [], "markers": [], "id": "el900014550916624", "ydomain": [-3.0, 3.0], "collections": [{"paths": [[[[0.0, -0.5], [0.13260155, -0.5], [0.25978993539242673, -0.44731684579412084], [0.3535533905932738, -0.3535533905932738], [0.44731684579412084, -0.25978993539242673], [0.5, -0.13260155], [0.5, 0.0], [0.5, 0.13260155], [0.44731684579412084, 0.25978993539242673], [0.3535533905932738, 0.3535533905932738], [0.25978993539242673, 0.44731684579412084], [0.13260155, 0.5], [0.0, 0.5], [-0.13260155, 0.5], [-0.25978993539242673, 0.44731684579412084], [-0.3535533905932738, 0.3535533905932738], [-0.44731684579412084, 0.25978993539242673], [-0.5, 0.13260155], [-0.5, 0.0], [-0.5, -0.13260155], [-0.44731684579412084, -0.25978993539242673], [-0.3535533905932738, -0.3535533905932738], [-0.25978993539242673, -0.44731684579412084], [-0.13260155, -0.5], [0.0, -0.5]], ["M", "C", "C", "C", "C", "C", "C", "C", "C", "Z"]]], "edgecolors": ["#000000"], "edgewidths": [0.3], "offsets": "data01", "yindex": 1, "id": "el900014599707536", "pathtransforms": [[4.969039949999533, 0.0, 0.0, 4.969039949999533, 0.0, 0.0]], "pathcoordinates": "display", "offsetcoordinates": "data", "zorder": 1, "xindex": 0, "alphas": [null], "facecolors": ["#0000FF"]}], "xscale": "linear", "bbox": [0.125, 0.65781250000000002, 0.2421875, 0.2421875]}, {"xlim": [-4.0, 4.0], "yscale": "linear", "axesbg": "#EAEAF2", "texts": [], "zoomable": true, "images": [], "xdomain": [-4.0, 4.0], "ylim": [-3.0, 3.0], "paths": [], "sharey": [], "sharex": [], "axesbgalpha": null, "axes": [{"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "bottom", "nticks": 9, "tickvalues": null}, {"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "left", "nticks": 7, "tickvalues": null}], "lines": [], "markers": [], "id": "el900014588475472", "ydomain": [-3.0, 3.0], "collections": [{"paths": [[[[0.0, -0.5], [0.13260155, -0.5], [0.25978993539242673, -0.44731684579412084], [0.3535533905932738, -0.3535533905932738], [0.44731684579412084, -0.25978993539242673], [0.5, -0.13260155], [0.5, 0.0], [0.5, 0.13260155], [0.44731684579412084, 0.25978993539242673], [0.3535533905932738, 0.3535533905932738], [0.25978993539242673, 0.44731684579412084], [0.13260155, 0.5], [0.0, 0.5], [-0.13260155, 0.5], [-0.25978993539242673, 0.44731684579412084], [-0.3535533905932738, 0.3535533905932738], [-0.44731684579412084, 0.25978993539242673], [-0.5, 0.13260155], [-0.5, 0.0], [-0.5, -0.13260155], [-0.44731684579412084, -0.25978993539242673], [-0.3535533905932738, -0.3535533905932738], [-0.25978993539242673, -0.44731684579412084], [-0.13260155, -0.5], [0.0, -0.5]], ["M", "C", "C", "C", "C", "C", "C", "C", "C", "Z"]]], "edgecolors": ["#000000"], "edgewidths": [0.3], "offsets": "data01", "yindex": 1, "id": "el900014599709520", "pathtransforms": [[4.969039949999533, 0.0, 0.0, 4.969039949999533, 0.0, 0.0]], "pathcoordinates": "display", "offsetcoordinates": "data", "zorder": 1, "xindex": 2, "alphas": [null], "facecolors": ["#0000FF"]}], "xscale": "linear", "bbox": [0.39140625000000001, 0.65781250000000002, 0.24218749999999994, 0.2421875]}, {"xlim": [-3.0, 3.0], "yscale": "linear", "axesbg": "#EAEAF2", "texts": [], "zoomable": true, "images": [], "xdomain": [-3.0, 3.0], "ylim": [-3.0, 3.0], "paths": [], "sharey": [], "sharex": [], "axesbgalpha": null, "axes": [{"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "bottom", "nticks": 7, "tickvalues": null}, {"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "left", "nticks": 7, "tickvalues": null}], "lines": [], "markers": [], "id": "el900014589019664", "ydomain": [-3.0, 3.0], "collections": [{"paths": [[[[0.0, -0.5], [0.13260155, -0.5], [0.25978993539242673, -0.44731684579412084], [0.3535533905932738, -0.3535533905932738], [0.44731684579412084, -0.25978993539242673], [0.5, -0.13260155], [0.5, 0.0], [0.5, 0.13260155], [0.44731684579412084, 0.25978993539242673], [0.3535533905932738, 0.3535533905932738], [0.25978993539242673, 0.44731684579412084], [0.13260155, 0.5], [0.0, 0.5], [-0.13260155, 0.5], [-0.25978993539242673, 0.44731684579412084], [-0.3535533905932738, 0.3535533905932738], [-0.44731684579412084, 0.25978993539242673], [-0.5, 0.13260155], [-0.5, 0.0], [-0.5, -0.13260155], [-0.44731684579412084, -0.25978993539242673], [-0.3535533905932738, -0.3535533905932738], [-0.25978993539242673, -0.44731684579412084], [-0.13260155, -0.5], [0.0, -0.5]], ["M", "C", "C", "C", "C", "C", "C", "C", "C", "Z"]]], "edgecolors": ["#000000"], "edgewidths": [0.3], "offsets": "data01", "yindex": 1, "id": "el900014594845648", "pathtransforms": [[4.969039949999533, 0.0, 0.0, 4.969039949999533, 0.0, 0.0]], "pathcoordinates": "display", "offsetcoordinates": "data", "zorder": 1, "xindex": 1, "alphas": [null], "facecolors": ["#0000FF"]}], "xscale": "linear", "bbox": [0.65781249999999991, 0.65781250000000002, 0.2421875, 0.2421875]}, {"xlim": [-3.0, 3.0], "yscale": "linear", "axesbg": "#EAEAF2", "texts": [], "zoomable": true, "images": [], "xdomain": [-3.0, 3.0], "ylim": [-4.0, 4.0], "paths": [], "sharey": [], "sharex": [], "axesbgalpha": null, "axes": [{"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "bottom", "nticks": 7, "tickvalues": null}, {"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "left", "nticks": 9, "tickvalues": null}], "lines": [], "markers": [], "id": "el900014590673040", "ydomain": [-4.0, 4.0], "collections": [{"paths": [[[[0.0, -0.5], [0.13260155, -0.5], [0.25978993539242673, -0.44731684579412084], [0.3535533905932738, -0.3535533905932738], [0.44731684579412084, -0.25978993539242673], [0.5, -0.13260155], [0.5, 0.0], [0.5, 0.13260155], [0.44731684579412084, 0.25978993539242673], [0.3535533905932738, 0.3535533905932738], [0.25978993539242673, 0.44731684579412084], [0.13260155, 0.5], [0.0, 0.5], [-0.13260155, 0.5], [-0.25978993539242673, 0.44731684579412084], [-0.3535533905932738, 0.3535533905932738], [-0.44731684579412084, 0.25978993539242673], [-0.5, 0.13260155], [-0.5, 0.0], [-0.5, -0.13260155], [-0.44731684579412084, -0.25978993539242673], [-0.3535533905932738, -0.3535533905932738], [-0.25978993539242673, -0.44731684579412084], [-0.13260155, -0.5], [0.0, -0.5]], ["M", "C", "C", "C", "C", "C", "C", "C", "C", "Z"]]], "edgecolors": ["#000000"], "edgewidths": [0.3], "offsets": "data01", "yindex": 2, "id": "el900014594847632", "pathtransforms": [[4.969039949999533, 0.0, 0.0, 4.969039949999533, 0.0, 0.0]], "pathcoordinates": "display", "offsetcoordinates": "data", "zorder": 1, "xindex": 0, "alphas": [null], "facecolors": ["#0000FF"]}], "xscale": "linear", "bbox": [0.125, 0.39140625000000007, 0.2421875, 0.24218749999999989]}, {"xlim": [-4.0, 4.0], "yscale": "linear", "axesbg": "#EAEAF2", "texts": [], "zoomable": true, "images": [], "xdomain": [-4.0, 4.0], "ylim": [-4.0, 4.0], "paths": [], "sharey": [], "sharex": [], "axesbgalpha": null, "axes": [{"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "bottom", "nticks": 9, "tickvalues": null}, {"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "left", "nticks": 9, "tickvalues": null}], "lines": [], "markers": [], "id": "el900014591252880", "ydomain": [-4.0, 4.0], "collections": [{"paths": [[[[0.0, -0.5], [0.13260155, -0.5], [0.25978993539242673, -0.44731684579412084], [0.3535533905932738, -0.3535533905932738], [0.44731684579412084, -0.25978993539242673], [0.5, -0.13260155], [0.5, 0.0], [0.5, 0.13260155], [0.44731684579412084, 0.25978993539242673], [0.3535533905932738, 0.3535533905932738], [0.25978993539242673, 0.44731684579412084], [0.13260155, 0.5], [0.0, 0.5], [-0.13260155, 0.5], [-0.25978993539242673, 0.44731684579412084], [-0.3535533905932738, 0.3535533905932738], [-0.44731684579412084, 0.25978993539242673], [-0.5, 0.13260155], [-0.5, 0.0], [-0.5, -0.13260155], [-0.44731684579412084, -0.25978993539242673], [-0.3535533905932738, -0.3535533905932738], [-0.25978993539242673, -0.44731684579412084], [-0.13260155, -0.5], [0.0, -0.5]], ["M", "C", "C", "C", "C", "C", "C", "C", "C", "Z"]]], "edgecolors": ["#000000"], "edgewidths": [0.3], "offsets": "data01", "yindex": 2, "id": "el900014599658192", "pathtransforms": [[4.969039949999533, 0.0, 0.0, 4.969039949999533, 0.0, 0.0]], "pathcoordinates": "display", "offsetcoordinates": "data", "zorder": 1, "xindex": 2, "alphas": [null], "facecolors": ["#0000FF"]}], "xscale": "linear", "bbox": [0.39140625000000001, 0.39140625000000007, 0.24218749999999994, 0.24218749999999989]}, {"xlim": [-3.0, 3.0], "yscale": "linear", "axesbg": "#EAEAF2", "texts": [], "zoomable": true, "images": [], "xdomain": [-3.0, 3.0], "ylim": [-4.0, 4.0], "paths": [], "sharey": [], "sharex": [], "axesbgalpha": null, "axes": [{"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "bottom", "nticks": 7, "tickvalues": null}, {"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "left", "nticks": 9, "tickvalues": null}], "lines": [], "markers": [], "id": "el900014591562704", "ydomain": [-4.0, 4.0], "collections": [{"paths": [[[[0.0, -0.5], [0.13260155, -0.5], [0.25978993539242673, -0.44731684579412084], [0.3535533905932738, -0.3535533905932738], [0.44731684579412084, -0.25978993539242673], [0.5, -0.13260155], [0.5, 0.0], [0.5, 0.13260155], [0.44731684579412084, 0.25978993539242673], [0.3535533905932738, 0.3535533905932738], [0.25978993539242673, 0.44731684579412084], [0.13260155, 0.5], [0.0, 0.5], [-0.13260155, 0.5], [-0.25978993539242673, 0.44731684579412084], [-0.3535533905932738, 0.3535533905932738], [-0.44731684579412084, 0.25978993539242673], [-0.5, 0.13260155], [-0.5, 0.0], [-0.5, -0.13260155], [-0.44731684579412084, -0.25978993539242673], [-0.3535533905932738, -0.3535533905932738], [-0.25978993539242673, -0.44731684579412084], [-0.13260155, -0.5], [0.0, -0.5]], ["M", "C", "C", "C", "C", "C", "C", "C", "C", "Z"]]], "edgecolors": ["#000000"], "edgewidths": [0.3], "offsets": "data01", "yindex": 2, "id": "el900014599660368", "pathtransforms": [[4.969039949999533, 0.0, 0.0, 4.969039949999533, 0.0, 0.0]], "pathcoordinates": "display", "offsetcoordinates": "data", "zorder": 1, "xindex": 1, "alphas": [null], "facecolors": ["#0000FF"]}], "xscale": "linear", "bbox": [0.65781249999999991, 0.39140625000000007, 0.2421875, 0.24218749999999989]}, {"xlim": [-3.0, 3.0], "yscale": "linear", "axesbg": "#EAEAF2", "texts": [], "zoomable": true, "images": [], "xdomain": [-3.0, 3.0], "ylim": [-3.0, 3.0], "paths": [], "sharey": [], "sharex": [], "axesbgalpha": null, "axes": [{"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "bottom", "nticks": 7, "tickvalues": null}, {"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "left", "nticks": 7, "tickvalues": null}], "lines": [], "markers": [], "id": "el900014592197968", "ydomain": [-3.0, 3.0], "collections": [{"paths": [[[[0.0, -0.5], [0.13260155, -0.5], [0.25978993539242673, -0.44731684579412084], [0.3535533905932738, -0.3535533905932738], [0.44731684579412084, -0.25978993539242673], [0.5, -0.13260155], [0.5, 0.0], [0.5, 0.13260155], [0.44731684579412084, 0.25978993539242673], [0.3535533905932738, 0.3535533905932738], [0.25978993539242673, 0.44731684579412084], [0.13260155, 0.5], [0.0, 0.5], [-0.13260155, 0.5], [-0.25978993539242673, 0.44731684579412084], [-0.3535533905932738, 0.3535533905932738], [-0.44731684579412084, 0.25978993539242673], [-0.5, 0.13260155], [-0.5, 0.0], [-0.5, -0.13260155], [-0.44731684579412084, -0.25978993539242673], [-0.3535533905932738, -0.3535533905932738], [-0.25978993539242673, -0.44731684579412084], [-0.13260155, -0.5], [0.0, -0.5]], ["M", "C", "C", "C", "C", "C", "C", "C", "C", "Z"]]], "edgecolors": ["#000000"], "edgewidths": [0.3], "offsets": "data01", "yindex": 0, "id": "el900014373148816", "pathtransforms": [[4.969039949999533, 0.0, 0.0, 4.969039949999533, 0.0, 0.0]], "pathcoordinates": "display", "offsetcoordinates": "data", "zorder": 1, "xindex": 0, "alphas": [null], "facecolors": ["#0000FF"]}], "xscale": "linear", "bbox": [0.125, 0.12500000000000011, 0.2421875, 0.2421875]}, {"xlim": [-4.0, 4.0], "yscale": "linear", "axesbg": "#EAEAF2", "texts": [], "zoomable": true, "images": [], "xdomain": [-4.0, 4.0], "ylim": [-3.0, 3.0], "paths": [], "sharey": [], "sharex": [], "axesbgalpha": null, "axes": [{"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "bottom", "nticks": 9, "tickvalues": null}, {"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "left", "nticks": 7, "tickvalues": null}], "lines": [], "markers": [], "id": "el900014592734416", "ydomain": [-3.0, 3.0], "collections": [{"paths": [[[[0.0, -0.5], [0.13260155, -0.5], [0.25978993539242673, -0.44731684579412084], [0.3535533905932738, -0.3535533905932738], [0.44731684579412084, -0.25978993539242673], [0.5, -0.13260155], [0.5, 0.0], [0.5, 0.13260155], [0.44731684579412084, 0.25978993539242673], [0.3535533905932738, 0.3535533905932738], [0.25978993539242673, 0.44731684579412084], [0.13260155, 0.5], [0.0, 0.5], [-0.13260155, 0.5], [-0.25978993539242673, 0.44731684579412084], [-0.3535533905932738, 0.3535533905932738], [-0.44731684579412084, 0.25978993539242673], [-0.5, 0.13260155], [-0.5, 0.0], [-0.5, -0.13260155], [-0.44731684579412084, -0.25978993539242673], [-0.3535533905932738, -0.3535533905932738], [-0.25978993539242673, -0.44731684579412084], [-0.13260155, -0.5], [0.0, -0.5]], ["M", "C", "C", "C", "C", "C", "C", "C", "C", "Z"]]], "edgecolors": ["#000000"], "edgewidths": [0.3], "offsets": "data01", "yindex": 0, "id": "el900014594761552", "pathtransforms": [[4.969039949999533, 0.0, 0.0, 4.969039949999533, 0.0, 0.0]], "pathcoordinates": "display", "offsetcoordinates": "data", "zorder": 1, "xindex": 2, "alphas": [null], "facecolors": ["#0000FF"]}], "xscale": "linear", "bbox": [0.39140625000000001, 0.12500000000000011, 0.24218749999999994, 0.2421875]}, {"xlim": [-3.0, 3.0], "yscale": "linear", "axesbg": "#EAEAF2", "texts": [], "zoomable": true, "images": [], "xdomain": [-3.0, 3.0], "ylim": [-3.0, 3.0], "paths": [], "sharey": [], "sharex": [], "axesbgalpha": null, "axes": [{"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "bottom", "nticks": 7, "tickvalues": null}, {"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "left", "nticks": 7, "tickvalues": null}], "lines": [], "markers": [], "id": "el900014594230032", "ydomain": [-3.0, 3.0], "collections": [{"paths": [[[[0.0, -0.5], [0.13260155, -0.5], [0.25978993539242673, -0.44731684579412084], [0.3535533905932738, -0.3535533905932738], [0.44731684579412084, -0.25978993539242673], [0.5, -0.13260155], [0.5, 0.0], [0.5, 0.13260155], [0.44731684579412084, 0.25978993539242673], [0.3535533905932738, 0.3535533905932738], [0.25978993539242673, 0.44731684579412084], [0.13260155, 0.5], [0.0, 0.5], [-0.13260155, 0.5], [-0.25978993539242673, 0.44731684579412084], [-0.3535533905932738, 0.3535533905932738], [-0.44731684579412084, 0.25978993539242673], [-0.5, 0.13260155], [-0.5, 0.0], [-0.5, -0.13260155], [-0.44731684579412084, -0.25978993539242673], [-0.3535533905932738, -0.3535533905932738], [-0.25978993539242673, -0.44731684579412084], [-0.13260155, -0.5], [0.0, -0.5]], ["M", "C", "C", "C", "C", "C", "C", "C", "C", "Z"]]], "edgecolors": ["#000000"], "edgewidths": [0.3], "offsets": "data01", "yindex": 0, "id": "el900014594845584", "pathtransforms": [[4.969039949999533, 0.0, 0.0, 4.969039949999533, 0.0, 0.0]], "pathcoordinates": "display", "offsetcoordinates": "data", "zorder": 1, "xindex": 1, "alphas": [null], "facecolors": ["#0000FF"]}], "xscale": "linear", "bbox": [0.65781249999999991, 0.12500000000000011, 0.2421875, 0.2421875]}], "height": 480.0, "width": 480.0, "plugins": [{"type": "reset"}, {"enabled": false, "button": true, "type": "zoom"}, {"enabled": false, "button": true, "type": "boxzoom"}, {"enabled": true, "button": true, "type": "linkedbrush", "id": "el900014594845648"}], "data": {"data01": [[0.72627725515196, -0.609617514020416, -0.5085678480094306], [0.45470011425609647, 0.5648926982935867, -0.07229420027544038], [-0.9124990804111092, 0.7810756401052897, 1.2812488443811665], [-0.7158326645558005, 0.25439416295376643, 0.31434136860601114], [-1.3243474989055997, -1.2952343469304026, 0.4754065777451255], [0.20679789169204818, 0.282404609880748, 1.3642822338969176], [-0.4557509822065865, -0.057390405349647504, 0.5354643397144171], [-0.6854256925510113, 1.2669241576729566, -0.481565174156881], [1.814654931930241, 0.18661309228043924, 0.9229610589958064], [0.052483512450695616, 0.3238070594522619, 1.4667236272430229], [0.13314946262202526, 0.32535765075875456, 0.39387343338897307], [0.44802397824046003, -0.3758686066043297, 0.792726218774311], [0.28838791256798113, -2.2127470505539173, 0.5951887985405865], [-0.04808559803838435, -0.012104520906811323, 1.050956950183763], [-0.8470614355031485, -1.1711151292027087, 1.4669946395869475], [0.5368092151501439, -0.7792166458718895, 0.07544892431309147], [1.4161306966828309, -1.7180110153349744, -0.4588268802293387], [-0.9318793884307652, 0.7125841349165489, 0.8655704499664272], [-0.10829885867639287, -0.9008733078048662, -1.3043377768214877], [-2.1120564133627213, -0.16195075185942912, 0.39739069661276416], [2.214811099602801, 0.9768731725614395, -0.6102095163636395], [1.4116382962479617, 1.2360207312265725, -0.9343642775454202], [0.09260686157586422, -1.1632633936028205, -0.2894947669214405], [1.0949929335337916, 0.4185271557657954, -0.8567939512184845], [-1.7348293757022026, -1.4919933255930191, -0.8381261398554098], [-1.1300231659030309, -0.027364650893653423, 0.11456105611135182], [0.04296811728542167, -0.2456817790822539, 0.23363478641727034], [-0.32799259057129415, 0.3451424424062806, 0.5700060750629162], [0.9255284017346328, -0.5670591322601339, 0.7750870513296308], [-0.08832214489077245, 0.29983404037903044, -1.0716826480772965], [-1.638834965530711, -0.38194204616313165, -1.136711044707441], [-0.5575665292820112, -0.08091792457355151, 0.6573602203284092], [0.37365684565744034, 0.3529559632748866, 0.2809258881984997], [0.4887378570322217, 0.1883181271903021, 0.48329021125635835], [0.17081981009178976, -0.3994384119083303, -2.898107886636492], [-0.41481003832437413, -0.15884641897830631, -0.7175629996855155], [0.5340501366272006, -0.32906501874691946, -0.4505594267519602], [-1.021849510491513, 1.1377134720591533, 0.4156376240675203], [-0.15542352142667828, 0.1466651626712377, 1.2817642340791557], [0.784914393549551, 0.0313394406364746, 1.4950548951738316], [-1.5481709714447207, -0.12901799786419965, -0.5330996829018881], [0.4369056050718823, 1.002751646087784, -2.4920690075337713], [1.5701115864102244, -1.6475363688431865, 0.6315677804318997], [1.0554867653362938, -0.2358060348147957, -3.266959888778148], [0.8404585908023985, 1.1581514499158168, 0.1663250543938972], [-0.7845963269487475, 0.33130543902850673, -0.3639803139134531], [0.45996385016833113, 1.4865079106239818, 1.886434068659524], [-0.5976399047987899, -0.4463228319216556, -0.5677397974228435], [-0.3103394440557323, 0.37498315078071864, 1.161281462047915], [1.436493430865783, -0.096681352504951, -1.2382134966592364], [-0.1277445046996717, -0.5040636724904181, -0.9672570417099028], [0.12646602176983848, 0.06999745869739371, 1.5593223284636468], [0.7238563827651077, -0.2582349724261488, 1.0803461260857055], [0.9627315040032325, 0.057620906905957496, 0.06964478084401315], [-0.24632853741784336, -0.3997498441462584, -1.3203974836871593], [-0.7920288712805237, -0.7140809170006572, 0.02088634706964818], [0.1805000557004198, -0.9420378333697007, 0.23586064317623523], [0.554405100440566, -0.28142207029323535, -1.0413287177771662], [0.853192500378185, 0.07035084063503451, 0.4816412277403756], [-0.4122852655096991, -0.6275094466917257, 0.6388292164357494], [-1.7916503324032693, 1.0611842309772412, 0.8043506198561388], [1.499128304380035, -0.22923354435393606, -0.6127739253326915], [0.5877440920038117, -0.09679831519842488, 0.7037686833116943], [0.9312481573556909, 1.2110140339067053, 1.1927568803146646], [0.3004882137247224, 0.20363007936894034, 0.14669002943773124], [-0.7252537272467792, 0.22320786239446536, 0.2687705443151357], [0.008929357633260495, 0.03930191858514528, -1.845114002105977], [0.8346320381668927, -0.3592331298055962, -0.28177403784654914], [-0.2029845612271129, 0.2963894804237323, 1.1564913912014636], [-0.24213933965518933, -1.9853205551530253, 1.1241320679288065], [1.2078111484101128, -0.04451501963175593, -0.33755740650598054], [0.02596642493816797, 0.5896365768471749, 1.7389086851206426], [-0.27272592823462677, -0.34694502323692084, -0.7267491032493013], [0.8705064224086991, 0.46208961203073134, -0.5412201434173727], [0.7858377646861028, 0.023582517005452063, 1.287438045339133], [1.1186765160237864, -1.5721953179179307, 0.89044155895576], [0.848459364855634, -0.0020518836814035343, -0.24644926739502987], [-1.4851792817789338, 0.025858139746513104, -0.009846715062858537], [0.22552813360915355, -0.38899731417893607, 0.2124520593062608], [1.868463602643709, -1.7619530684258848, 0.21475370107315214], [1.0982756880470732, 0.1452010110903084, 0.959355656855051], [0.2469251659721454, -0.29950036079570996, 0.3866760347184457], [0.5550636636168365, -0.07615493442218282, -1.3578999695134073], [-1.1511075167215055, 2.0130702386861214, 1.279947838742059], [-1.230231563968042, 0.5001903412542189, -1.0675891820283898], [-0.48506000456981535, 1.265567266053854, 2.082812115181861], [0.11879725907101205, 0.037140537822488516, -0.3114435839006701], [1.4902779255597118, 2.1297700734265836, 3.400046164356916], [-0.24172607361743356, 0.4004615150134686, -1.242510123566507], [1.6010966219497424, -0.6358910636344438, -0.6031516122144578], [1.386781576515262, -0.48026285883108716, 0.4795284854474212], [2.11299658582516, 0.986205002091192, -0.6816854976351491], [0.7709267112876348, 0.05610026154512464, 0.09272792278109766], [-0.14758532866242421, 1.0385928872415382, -0.46868766931818967], [1.8795447180644578, 0.17071962626703338, 0.012511656685759506], [1.0897120893968824, -0.9756555432684259, -2.429807661934103], [1.5166904646735573, 0.2132197913199486, 0.12465716254859609], [-0.7788432764438152, 1.1472826421052982, -1.0814674209098705], [0.2916684245546782, -0.19838535621231929, -0.7555625626768224], [-0.40415989019521464, 0.6620745944507938, -0.13301100501957958]]}, "id": "el900014550914768"});
          });
        });
    }else{
        // require.js not available: dynamically load d3 & mpld3
        mpld3_load_lib("https://mpld3.github.io/js/d3.v3.min.js", function(){
             mpld3_load_lib("https://mpld3.github.io/js/mpld3.v0.2.js", function(){
                     
                     mpld3.draw_figure("fig_el9000145509147684824814976", {"axes": [{"xlim": [-3.0, 3.0], "yscale": "linear", "axesbg": "#EAEAF2", "texts": [], "zoomable": true, "images": [], "xdomain": [-3.0, 3.0], "ylim": [-3.0, 3.0], "paths": [], "sharey": [], "sharex": [], "axesbgalpha": null, "axes": [{"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "bottom", "nticks": 7, "tickvalues": null}, {"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "left", "nticks": 7, "tickvalues": null}], "lines": [], "markers": [], "id": "el900014550916624", "ydomain": [-3.0, 3.0], "collections": [{"paths": [[[[0.0, -0.5], [0.13260155, -0.5], [0.25978993539242673, -0.44731684579412084], [0.3535533905932738, -0.3535533905932738], [0.44731684579412084, -0.25978993539242673], [0.5, -0.13260155], [0.5, 0.0], [0.5, 0.13260155], [0.44731684579412084, 0.25978993539242673], [0.3535533905932738, 0.3535533905932738], [0.25978993539242673, 0.44731684579412084], [0.13260155, 0.5], [0.0, 0.5], [-0.13260155, 0.5], [-0.25978993539242673, 0.44731684579412084], [-0.3535533905932738, 0.3535533905932738], [-0.44731684579412084, 0.25978993539242673], [-0.5, 0.13260155], [-0.5, 0.0], [-0.5, -0.13260155], [-0.44731684579412084, -0.25978993539242673], [-0.3535533905932738, -0.3535533905932738], [-0.25978993539242673, -0.44731684579412084], [-0.13260155, -0.5], [0.0, -0.5]], ["M", "C", "C", "C", "C", "C", "C", "C", "C", "Z"]]], "edgecolors": ["#000000"], "edgewidths": [0.3], "offsets": "data01", "yindex": 1, "id": "el900014599707536", "pathtransforms": [[4.969039949999533, 0.0, 0.0, 4.969039949999533, 0.0, 0.0]], "pathcoordinates": "display", "offsetcoordinates": "data", "zorder": 1, "xindex": 0, "alphas": [null], "facecolors": ["#0000FF"]}], "xscale": "linear", "bbox": [0.125, 0.65781250000000002, 0.2421875, 0.2421875]}, {"xlim": [-4.0, 4.0], "yscale": "linear", "axesbg": "#EAEAF2", "texts": [], "zoomable": true, "images": [], "xdomain": [-4.0, 4.0], "ylim": [-3.0, 3.0], "paths": [], "sharey": [], "sharex": [], "axesbgalpha": null, "axes": [{"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "bottom", "nticks": 9, "tickvalues": null}, {"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "left", "nticks": 7, "tickvalues": null}], "lines": [], "markers": [], "id": "el900014588475472", "ydomain": [-3.0, 3.0], "collections": [{"paths": [[[[0.0, -0.5], [0.13260155, -0.5], [0.25978993539242673, -0.44731684579412084], [0.3535533905932738, -0.3535533905932738], [0.44731684579412084, -0.25978993539242673], [0.5, -0.13260155], [0.5, 0.0], [0.5, 0.13260155], [0.44731684579412084, 0.25978993539242673], [0.3535533905932738, 0.3535533905932738], [0.25978993539242673, 0.44731684579412084], [0.13260155, 0.5], [0.0, 0.5], [-0.13260155, 0.5], [-0.25978993539242673, 0.44731684579412084], [-0.3535533905932738, 0.3535533905932738], [-0.44731684579412084, 0.25978993539242673], [-0.5, 0.13260155], [-0.5, 0.0], [-0.5, -0.13260155], [-0.44731684579412084, -0.25978993539242673], [-0.3535533905932738, -0.3535533905932738], [-0.25978993539242673, -0.44731684579412084], [-0.13260155, -0.5], [0.0, -0.5]], ["M", "C", "C", "C", "C", "C", "C", "C", "C", "Z"]]], "edgecolors": ["#000000"], "edgewidths": [0.3], "offsets": "data01", "yindex": 1, "id": "el900014599709520", "pathtransforms": [[4.969039949999533, 0.0, 0.0, 4.969039949999533, 0.0, 0.0]], "pathcoordinates": "display", "offsetcoordinates": "data", "zorder": 1, "xindex": 2, "alphas": [null], "facecolors": ["#0000FF"]}], "xscale": "linear", "bbox": [0.39140625000000001, 0.65781250000000002, 0.24218749999999994, 0.2421875]}, {"xlim": [-3.0, 3.0], "yscale": "linear", "axesbg": "#EAEAF2", "texts": [], "zoomable": true, "images": [], "xdomain": [-3.0, 3.0], "ylim": [-3.0, 3.0], "paths": [], "sharey": [], "sharex": [], "axesbgalpha": null, "axes": [{"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "bottom", "nticks": 7, "tickvalues": null}, {"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "left", "nticks": 7, "tickvalues": null}], "lines": [], "markers": [], "id": "el900014589019664", "ydomain": [-3.0, 3.0], "collections": [{"paths": [[[[0.0, -0.5], [0.13260155, -0.5], [0.25978993539242673, -0.44731684579412084], [0.3535533905932738, -0.3535533905932738], [0.44731684579412084, -0.25978993539242673], [0.5, -0.13260155], [0.5, 0.0], [0.5, 0.13260155], [0.44731684579412084, 0.25978993539242673], [0.3535533905932738, 0.3535533905932738], [0.25978993539242673, 0.44731684579412084], [0.13260155, 0.5], [0.0, 0.5], [-0.13260155, 0.5], [-0.25978993539242673, 0.44731684579412084], [-0.3535533905932738, 0.3535533905932738], [-0.44731684579412084, 0.25978993539242673], [-0.5, 0.13260155], [-0.5, 0.0], [-0.5, -0.13260155], [-0.44731684579412084, -0.25978993539242673], [-0.3535533905932738, -0.3535533905932738], [-0.25978993539242673, -0.44731684579412084], [-0.13260155, -0.5], [0.0, -0.5]], ["M", "C", "C", "C", "C", "C", "C", "C", "C", "Z"]]], "edgecolors": ["#000000"], "edgewidths": [0.3], "offsets": "data01", "yindex": 1, "id": "el900014594845648", "pathtransforms": [[4.969039949999533, 0.0, 0.0, 4.969039949999533, 0.0, 0.0]], "pathcoordinates": "display", "offsetcoordinates": "data", "zorder": 1, "xindex": 1, "alphas": [null], "facecolors": ["#0000FF"]}], "xscale": "linear", "bbox": [0.65781249999999991, 0.65781250000000002, 0.2421875, 0.2421875]}, {"xlim": [-3.0, 3.0], "yscale": "linear", "axesbg": "#EAEAF2", "texts": [], "zoomable": true, "images": [], "xdomain": [-3.0, 3.0], "ylim": [-4.0, 4.0], "paths": [], "sharey": [], "sharex": [], "axesbgalpha": null, "axes": [{"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "bottom", "nticks": 7, "tickvalues": null}, {"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "left", "nticks": 9, "tickvalues": null}], "lines": [], "markers": [], "id": "el900014590673040", "ydomain": [-4.0, 4.0], "collections": [{"paths": [[[[0.0, -0.5], [0.13260155, -0.5], [0.25978993539242673, -0.44731684579412084], [0.3535533905932738, -0.3535533905932738], [0.44731684579412084, -0.25978993539242673], [0.5, -0.13260155], [0.5, 0.0], [0.5, 0.13260155], [0.44731684579412084, 0.25978993539242673], [0.3535533905932738, 0.3535533905932738], [0.25978993539242673, 0.44731684579412084], [0.13260155, 0.5], [0.0, 0.5], [-0.13260155, 0.5], [-0.25978993539242673, 0.44731684579412084], [-0.3535533905932738, 0.3535533905932738], [-0.44731684579412084, 0.25978993539242673], [-0.5, 0.13260155], [-0.5, 0.0], [-0.5, -0.13260155], [-0.44731684579412084, -0.25978993539242673], [-0.3535533905932738, -0.3535533905932738], [-0.25978993539242673, -0.44731684579412084], [-0.13260155, -0.5], [0.0, -0.5]], ["M", "C", "C", "C", "C", "C", "C", "C", "C", "Z"]]], "edgecolors": ["#000000"], "edgewidths": [0.3], "offsets": "data01", "yindex": 2, "id": "el900014594847632", "pathtransforms": [[4.969039949999533, 0.0, 0.0, 4.969039949999533, 0.0, 0.0]], "pathcoordinates": "display", "offsetcoordinates": "data", "zorder": 1, "xindex": 0, "alphas": [null], "facecolors": ["#0000FF"]}], "xscale": "linear", "bbox": [0.125, 0.39140625000000007, 0.2421875, 0.24218749999999989]}, {"xlim": [-4.0, 4.0], "yscale": "linear", "axesbg": "#EAEAF2", "texts": [], "zoomable": true, "images": [], "xdomain": [-4.0, 4.0], "ylim": [-4.0, 4.0], "paths": [], "sharey": [], "sharex": [], "axesbgalpha": null, "axes": [{"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "bottom", "nticks": 9, "tickvalues": null}, {"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "left", "nticks": 9, "tickvalues": null}], "lines": [], "markers": [], "id": "el900014591252880", "ydomain": [-4.0, 4.0], "collections": [{"paths": [[[[0.0, -0.5], [0.13260155, -0.5], [0.25978993539242673, -0.44731684579412084], [0.3535533905932738, -0.3535533905932738], [0.44731684579412084, -0.25978993539242673], [0.5, -0.13260155], [0.5, 0.0], [0.5, 0.13260155], [0.44731684579412084, 0.25978993539242673], [0.3535533905932738, 0.3535533905932738], [0.25978993539242673, 0.44731684579412084], [0.13260155, 0.5], [0.0, 0.5], [-0.13260155, 0.5], [-0.25978993539242673, 0.44731684579412084], [-0.3535533905932738, 0.3535533905932738], [-0.44731684579412084, 0.25978993539242673], [-0.5, 0.13260155], [-0.5, 0.0], [-0.5, -0.13260155], [-0.44731684579412084, -0.25978993539242673], [-0.3535533905932738, -0.3535533905932738], [-0.25978993539242673, -0.44731684579412084], [-0.13260155, -0.5], [0.0, -0.5]], ["M", "C", "C", "C", "C", "C", "C", "C", "C", "Z"]]], "edgecolors": ["#000000"], "edgewidths": [0.3], "offsets": "data01", "yindex": 2, "id": "el900014599658192", "pathtransforms": [[4.969039949999533, 0.0, 0.0, 4.969039949999533, 0.0, 0.0]], "pathcoordinates": "display", "offsetcoordinates": "data", "zorder": 1, "xindex": 2, "alphas": [null], "facecolors": ["#0000FF"]}], "xscale": "linear", "bbox": [0.39140625000000001, 0.39140625000000007, 0.24218749999999994, 0.24218749999999989]}, {"xlim": [-3.0, 3.0], "yscale": "linear", "axesbg": "#EAEAF2", "texts": [], "zoomable": true, "images": [], "xdomain": [-3.0, 3.0], "ylim": [-4.0, 4.0], "paths": [], "sharey": [], "sharex": [], "axesbgalpha": null, "axes": [{"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "bottom", "nticks": 7, "tickvalues": null}, {"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "left", "nticks": 9, "tickvalues": null}], "lines": [], "markers": [], "id": "el900014591562704", "ydomain": [-4.0, 4.0], "collections": [{"paths": [[[[0.0, -0.5], [0.13260155, -0.5], [0.25978993539242673, -0.44731684579412084], [0.3535533905932738, -0.3535533905932738], [0.44731684579412084, -0.25978993539242673], [0.5, -0.13260155], [0.5, 0.0], [0.5, 0.13260155], [0.44731684579412084, 0.25978993539242673], [0.3535533905932738, 0.3535533905932738], [0.25978993539242673, 0.44731684579412084], [0.13260155, 0.5], [0.0, 0.5], [-0.13260155, 0.5], [-0.25978993539242673, 0.44731684579412084], [-0.3535533905932738, 0.3535533905932738], [-0.44731684579412084, 0.25978993539242673], [-0.5, 0.13260155], [-0.5, 0.0], [-0.5, -0.13260155], [-0.44731684579412084, -0.25978993539242673], [-0.3535533905932738, -0.3535533905932738], [-0.25978993539242673, -0.44731684579412084], [-0.13260155, -0.5], [0.0, -0.5]], ["M", "C", "C", "C", "C", "C", "C", "C", "C", "Z"]]], "edgecolors": ["#000000"], "edgewidths": [0.3], "offsets": "data01", "yindex": 2, "id": "el900014599660368", "pathtransforms": [[4.969039949999533, 0.0, 0.0, 4.969039949999533, 0.0, 0.0]], "pathcoordinates": "display", "offsetcoordinates": "data", "zorder": 1, "xindex": 1, "alphas": [null], "facecolors": ["#0000FF"]}], "xscale": "linear", "bbox": [0.65781249999999991, 0.39140625000000007, 0.2421875, 0.24218749999999989]}, {"xlim": [-3.0, 3.0], "yscale": "linear", "axesbg": "#EAEAF2", "texts": [], "zoomable": true, "images": [], "xdomain": [-3.0, 3.0], "ylim": [-3.0, 3.0], "paths": [], "sharey": [], "sharex": [], "axesbgalpha": null, "axes": [{"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "bottom", "nticks": 7, "tickvalues": null}, {"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "left", "nticks": 7, "tickvalues": null}], "lines": [], "markers": [], "id": "el900014592197968", "ydomain": [-3.0, 3.0], "collections": [{"paths": [[[[0.0, -0.5], [0.13260155, -0.5], [0.25978993539242673, -0.44731684579412084], [0.3535533905932738, -0.3535533905932738], [0.44731684579412084, -0.25978993539242673], [0.5, -0.13260155], [0.5, 0.0], [0.5, 0.13260155], [0.44731684579412084, 0.25978993539242673], [0.3535533905932738, 0.3535533905932738], [0.25978993539242673, 0.44731684579412084], [0.13260155, 0.5], [0.0, 0.5], [-0.13260155, 0.5], [-0.25978993539242673, 0.44731684579412084], [-0.3535533905932738, 0.3535533905932738], [-0.44731684579412084, 0.25978993539242673], [-0.5, 0.13260155], [-0.5, 0.0], [-0.5, -0.13260155], [-0.44731684579412084, -0.25978993539242673], [-0.3535533905932738, -0.3535533905932738], [-0.25978993539242673, -0.44731684579412084], [-0.13260155, -0.5], [0.0, -0.5]], ["M", "C", "C", "C", "C", "C", "C", "C", "C", "Z"]]], "edgecolors": ["#000000"], "edgewidths": [0.3], "offsets": "data01", "yindex": 0, "id": "el900014373148816", "pathtransforms": [[4.969039949999533, 0.0, 0.0, 4.969039949999533, 0.0, 0.0]], "pathcoordinates": "display", "offsetcoordinates": "data", "zorder": 1, "xindex": 0, "alphas": [null], "facecolors": ["#0000FF"]}], "xscale": "linear", "bbox": [0.125, 0.12500000000000011, 0.2421875, 0.2421875]}, {"xlim": [-4.0, 4.0], "yscale": "linear", "axesbg": "#EAEAF2", "texts": [], "zoomable": true, "images": [], "xdomain": [-4.0, 4.0], "ylim": [-3.0, 3.0], "paths": [], "sharey": [], "sharex": [], "axesbgalpha": null, "axes": [{"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "bottom", "nticks": 9, "tickvalues": null}, {"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "left", "nticks": 7, "tickvalues": null}], "lines": [], "markers": [], "id": "el900014592734416", "ydomain": [-3.0, 3.0], "collections": [{"paths": [[[[0.0, -0.5], [0.13260155, -0.5], [0.25978993539242673, -0.44731684579412084], [0.3535533905932738, -0.3535533905932738], [0.44731684579412084, -0.25978993539242673], [0.5, -0.13260155], [0.5, 0.0], [0.5, 0.13260155], [0.44731684579412084, 0.25978993539242673], [0.3535533905932738, 0.3535533905932738], [0.25978993539242673, 0.44731684579412084], [0.13260155, 0.5], [0.0, 0.5], [-0.13260155, 0.5], [-0.25978993539242673, 0.44731684579412084], [-0.3535533905932738, 0.3535533905932738], [-0.44731684579412084, 0.25978993539242673], [-0.5, 0.13260155], [-0.5, 0.0], [-0.5, -0.13260155], [-0.44731684579412084, -0.25978993539242673], [-0.3535533905932738, -0.3535533905932738], [-0.25978993539242673, -0.44731684579412084], [-0.13260155, -0.5], [0.0, -0.5]], ["M", "C", "C", "C", "C", "C", "C", "C", "C", "Z"]]], "edgecolors": ["#000000"], "edgewidths": [0.3], "offsets": "data01", "yindex": 0, "id": "el900014594761552", "pathtransforms": [[4.969039949999533, 0.0, 0.0, 4.969039949999533, 0.0, 0.0]], "pathcoordinates": "display", "offsetcoordinates": "data", "zorder": 1, "xindex": 2, "alphas": [null], "facecolors": ["#0000FF"]}], "xscale": "linear", "bbox": [0.39140625000000001, 0.12500000000000011, 0.24218749999999994, 0.2421875]}, {"xlim": [-3.0, 3.0], "yscale": "linear", "axesbg": "#EAEAF2", "texts": [], "zoomable": true, "images": [], "xdomain": [-3.0, 3.0], "ylim": [-3.0, 3.0], "paths": [], "sharey": [], "sharex": [], "axesbgalpha": null, "axes": [{"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "bottom", "nticks": 7, "tickvalues": null}, {"scale": "linear", "tickformat": "", "grid": {"color": "#FFFFFF", "alpha": 1.0, "dasharray": "10,0", "gridOn": true}, "fontsize": 10.0, "position": "left", "nticks": 7, "tickvalues": null}], "lines": [], "markers": [], "id": "el900014594230032", "ydomain": [-3.0, 3.0], "collections": [{"paths": [[[[0.0, -0.5], [0.13260155, -0.5], [0.25978993539242673, -0.44731684579412084], [0.3535533905932738, -0.3535533905932738], [0.44731684579412084, -0.25978993539242673], [0.5, -0.13260155], [0.5, 0.0], [0.5, 0.13260155], [0.44731684579412084, 0.25978993539242673], [0.3535533905932738, 0.3535533905932738], [0.25978993539242673, 0.44731684579412084], [0.13260155, 0.5], [0.0, 0.5], [-0.13260155, 0.5], [-0.25978993539242673, 0.44731684579412084], [-0.3535533905932738, 0.3535533905932738], [-0.44731684579412084, 0.25978993539242673], [-0.5, 0.13260155], [-0.5, 0.0], [-0.5, -0.13260155], [-0.44731684579412084, -0.25978993539242673], [-0.3535533905932738, -0.3535533905932738], [-0.25978993539242673, -0.44731684579412084], [-0.13260155, -0.5], [0.0, -0.5]], ["M", "C", "C", "C", "C", "C", "C", "C", "C", "Z"]]], "edgecolors": ["#000000"], "edgewidths": [0.3], "offsets": "data01", "yindex": 0, "id": "el900014594845584", "pathtransforms": [[4.969039949999533, 0.0, 0.0, 4.969039949999533, 0.0, 0.0]], "pathcoordinates": "display", "offsetcoordinates": "data", "zorder": 1, "xindex": 1, "alphas": [null], "facecolors": ["#0000FF"]}], "xscale": "linear", "bbox": [0.65781249999999991, 0.12500000000000011, 0.2421875, 0.2421875]}], "height": 480.0, "width": 480.0, "plugins": [{"type": "reset"}, {"enabled": false, "button": true, "type": "zoom"}, {"enabled": false, "button": true, "type": "boxzoom"}, {"enabled": true, "button": true, "type": "linkedbrush", "id": "el900014594845648"}], "data": {"data01": [[0.72627725515196, -0.609617514020416, -0.5085678480094306], [0.45470011425609647, 0.5648926982935867, -0.07229420027544038], [-0.9124990804111092, 0.7810756401052897, 1.2812488443811665], [-0.7158326645558005, 0.25439416295376643, 0.31434136860601114], [-1.3243474989055997, -1.2952343469304026, 0.4754065777451255], [0.20679789169204818, 0.282404609880748, 1.3642822338969176], [-0.4557509822065865, -0.057390405349647504, 0.5354643397144171], [-0.6854256925510113, 1.2669241576729566, -0.481565174156881], [1.814654931930241, 0.18661309228043924, 0.9229610589958064], [0.052483512450695616, 0.3238070594522619, 1.4667236272430229], [0.13314946262202526, 0.32535765075875456, 0.39387343338897307], [0.44802397824046003, -0.3758686066043297, 0.792726218774311], [0.28838791256798113, -2.2127470505539173, 0.5951887985405865], [-0.04808559803838435, -0.012104520906811323, 1.050956950183763], [-0.8470614355031485, -1.1711151292027087, 1.4669946395869475], [0.5368092151501439, -0.7792166458718895, 0.07544892431309147], [1.4161306966828309, -1.7180110153349744, -0.4588268802293387], [-0.9318793884307652, 0.7125841349165489, 0.8655704499664272], [-0.10829885867639287, -0.9008733078048662, -1.3043377768214877], [-2.1120564133627213, -0.16195075185942912, 0.39739069661276416], [2.214811099602801, 0.9768731725614395, -0.6102095163636395], [1.4116382962479617, 1.2360207312265725, -0.9343642775454202], [0.09260686157586422, -1.1632633936028205, -0.2894947669214405], [1.0949929335337916, 0.4185271557657954, -0.8567939512184845], [-1.7348293757022026, -1.4919933255930191, -0.8381261398554098], [-1.1300231659030309, -0.027364650893653423, 0.11456105611135182], [0.04296811728542167, -0.2456817790822539, 0.23363478641727034], [-0.32799259057129415, 0.3451424424062806, 0.5700060750629162], [0.9255284017346328, -0.5670591322601339, 0.7750870513296308], [-0.08832214489077245, 0.29983404037903044, -1.0716826480772965], [-1.638834965530711, -0.38194204616313165, -1.136711044707441], [-0.5575665292820112, -0.08091792457355151, 0.6573602203284092], [0.37365684565744034, 0.3529559632748866, 0.2809258881984997], [0.4887378570322217, 0.1883181271903021, 0.48329021125635835], [0.17081981009178976, -0.3994384119083303, -2.898107886636492], [-0.41481003832437413, -0.15884641897830631, -0.7175629996855155], [0.5340501366272006, -0.32906501874691946, -0.4505594267519602], [-1.021849510491513, 1.1377134720591533, 0.4156376240675203], [-0.15542352142667828, 0.1466651626712377, 1.2817642340791557], [0.784914393549551, 0.0313394406364746, 1.4950548951738316], [-1.5481709714447207, -0.12901799786419965, -0.5330996829018881], [0.4369056050718823, 1.002751646087784, -2.4920690075337713], [1.5701115864102244, -1.6475363688431865, 0.6315677804318997], [1.0554867653362938, -0.2358060348147957, -3.266959888778148], [0.8404585908023985, 1.1581514499158168, 0.1663250543938972], [-0.7845963269487475, 0.33130543902850673, -0.3639803139134531], [0.45996385016833113, 1.4865079106239818, 1.886434068659524], [-0.5976399047987899, -0.4463228319216556, -0.5677397974228435], [-0.3103394440557323, 0.37498315078071864, 1.161281462047915], [1.436493430865783, -0.096681352504951, -1.2382134966592364], [-0.1277445046996717, -0.5040636724904181, -0.9672570417099028], [0.12646602176983848, 0.06999745869739371, 1.5593223284636468], [0.7238563827651077, -0.2582349724261488, 1.0803461260857055], [0.9627315040032325, 0.057620906905957496, 0.06964478084401315], [-0.24632853741784336, -0.3997498441462584, -1.3203974836871593], [-0.7920288712805237, -0.7140809170006572, 0.02088634706964818], [0.1805000557004198, -0.9420378333697007, 0.23586064317623523], [0.554405100440566, -0.28142207029323535, -1.0413287177771662], [0.853192500378185, 0.07035084063503451, 0.4816412277403756], [-0.4122852655096991, -0.6275094466917257, 0.6388292164357494], [-1.7916503324032693, 1.0611842309772412, 0.8043506198561388], [1.499128304380035, -0.22923354435393606, -0.6127739253326915], [0.5877440920038117, -0.09679831519842488, 0.7037686833116943], [0.9312481573556909, 1.2110140339067053, 1.1927568803146646], [0.3004882137247224, 0.20363007936894034, 0.14669002943773124], [-0.7252537272467792, 0.22320786239446536, 0.2687705443151357], [0.008929357633260495, 0.03930191858514528, -1.845114002105977], [0.8346320381668927, -0.3592331298055962, -0.28177403784654914], [-0.2029845612271129, 0.2963894804237323, 1.1564913912014636], [-0.24213933965518933, -1.9853205551530253, 1.1241320679288065], [1.2078111484101128, -0.04451501963175593, -0.33755740650598054], [0.02596642493816797, 0.5896365768471749, 1.7389086851206426], [-0.27272592823462677, -0.34694502323692084, -0.7267491032493013], [0.8705064224086991, 0.46208961203073134, -0.5412201434173727], [0.7858377646861028, 0.023582517005452063, 1.287438045339133], [1.1186765160237864, -1.5721953179179307, 0.89044155895576], [0.848459364855634, -0.0020518836814035343, -0.24644926739502987], [-1.4851792817789338, 0.025858139746513104, -0.009846715062858537], [0.22552813360915355, -0.38899731417893607, 0.2124520593062608], [1.868463602643709, -1.7619530684258848, 0.21475370107315214], [1.0982756880470732, 0.1452010110903084, 0.959355656855051], [0.2469251659721454, -0.29950036079570996, 0.3866760347184457], [0.5550636636168365, -0.07615493442218282, -1.3578999695134073], [-1.1511075167215055, 2.0130702386861214, 1.279947838742059], [-1.230231563968042, 0.5001903412542189, -1.0675891820283898], [-0.48506000456981535, 1.265567266053854, 2.082812115181861], [0.11879725907101205, 0.037140537822488516, -0.3114435839006701], [1.4902779255597118, 2.1297700734265836, 3.400046164356916], [-0.24172607361743356, 0.4004615150134686, -1.242510123566507], [1.6010966219497424, -0.6358910636344438, -0.6031516122144578], [1.386781576515262, -0.48026285883108716, 0.4795284854474212], [2.11299658582516, 0.986205002091192, -0.6816854976351491], [0.7709267112876348, 0.05610026154512464, 0.09272792278109766], [-0.14758532866242421, 1.0385928872415382, -0.46868766931818967], [1.8795447180644578, 0.17071962626703338, 0.012511656685759506], [1.0897120893968824, -0.9756555432684259, -2.429807661934103], [1.5166904646735573, 0.2132197913199486, 0.12465716254859609], [-0.7788432764438152, 1.1472826421052982, -1.0814674209098705], [0.2916684245546782, -0.19838535621231929, -0.7555625626768224], [-0.40415989019521464, 0.6620745944507938, -0.13301100501957958]]}, "id": "el900014550914768"});
                })
             });
    }
    </script>


