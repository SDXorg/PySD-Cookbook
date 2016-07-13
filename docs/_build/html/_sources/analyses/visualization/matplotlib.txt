
Basic Visualization with ``matplotlib``
=======================================

Python's most commonly used plotting library is
`matplotlib <http://matplotlib.org/>`__. The library has an interface
which mirrors that of Mathworks'
`Matlab <http://www.mathworks.com/help/matlab/2-and-3d-plots.html>`__
software, and so those with matlab familiarity will find themselves
already high up on the learning curve.

Loading ``matplotlib`` and setting up the notebook environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The matplotlib plotting library has a
`magic <https://ipython.org/ipython-doc/3/interactive/magics.html#magic-pylab>`__
connection with the iPython shell and the notebook environment that
allows static images of plots to be rendered in the notebook. Instead of
using the normal ``import ...`` syntax, we'll use this iPython 'magic'
to not only import the library, but set up the environment we'll need to
create plots.

.. code:: python

    %pylab inline


.. parsed-literal::

    Populating the interactive namespace from numpy and matplotlib


Load data to plot
~~~~~~~~~~~~~~~~~

We'll use the emissions data we saw before in the Pandas tutorial, as
it's familiar:

.. code:: python

    import pandas as pd
    emissions = pd.read_csv('../../data/Climate/global_emissions.csv', 
                            skiprows=2, index_col='Year',
                            names=['Year', 'Total Emissions', 
                                   'Gas Emissions', 'Liquid Emissions', 
                                   'Solid Emissions', 'Cement Emissions', 
                                   'Flare Emissions', 'Per Capita Emissions'])
    
    emissions.head(3)


.. parsed-literal::

    /Users/houghton/anaconda/lib/python2.7/site-packages/pandas/computation/__init__.py:19: UserWarning: The installed version of numexpr 2.4.4 is not supported in pandas and will be not be used
    
      UserWarning)




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
      </tbody>
    </table>
    </div>



Basic plotting
~~~~~~~~~~~~~~

The basic plot command takes as its first two arguments the x and y
values of the points which we wish to plot:

.. code:: python

    plt.plot(emissions.index, emissions['Total Emissions']);



.. image:: matplotlib_files/matplotlib_6_0.png


Labeling axes and title
~~~~~~~~~~~~~~~~~~~~~~~

Following out plot command we can submit commands to `add text to the
figure <http://matplotlib.org/users/pyplot_tutorial.html#working-with-text>`__,
such as adding labels to the x and y axes, and a title to the figure.

.. code:: python

    plt.plot(emissions.index, emissions['Total Emissions'])
    plt.xlabel('Year')
    plt.ylabel('Million Metric Tons CO2/Year')
    plt.title('Historical CO2 Emissions', fontsize=18);



.. image:: matplotlib_files/matplotlib_8_0.png


Changing line properties
~~~~~~~~~~~~~~~~~~~~~~~~

We can include various elements into the plot command to `specify how
the line will
look <http://matplotlib.org/users/pyplot_tutorial.html#controlling-line-properties>`__:

.. code:: python

    plt.plot(emissions.index, emissions['Total Emissions'], 'ro', alpha=.5);



.. image:: matplotlib_files/matplotlib_10_0.png


Specifying axis bounds
~~~~~~~~~~~~~~~~~~~~~~

We can specify that we want our plot to be bounded by various x and y
values:

.. code:: python

    plt.plot(emissions.index, emissions['Total Emissions'])
    plt.xlim(1950,2000)
    plt.ylim(1500,7500);



.. image:: matplotlib_files/matplotlib_12_0.png


Multiple lines
~~~~~~~~~~~~~~

We can add lines to our plot simply by adding additional calls to the
plot function. Passing the plot function an argument called 'label'
allows us to format a
`legend <http://matplotlib.org/users/legend_guide.html>`__ with
appropriate references to each line:

.. code:: python

    plt.plot(emissions.index, emissions['Liquid Emissions'], 'r', label='Liquid')
    plt.plot(emissions.index, emissions['Solid Emissions'], 'b', label='Solid')
    plt.plot(emissions.index, emissions['Gas Emissions'], 'g', label='Gas')
    plt.legend(loc='upper left');



.. image:: matplotlib_files/matplotlib_14_0.png


Other plot types
~~~~~~~~~~~~~~~~

There are a number of other plot types available, such as histograms,
radial plots, plots with logarithmic axes, or stackplots:

.. code:: python

    plt.stackplot(emissions.index, [emissions['Liquid Emissions'], 
                                    emissions['Gas Emissions'],
                                    emissions['Solid Emissions']],
                 labels=['Liquid', 'Gas', 'Solid'])
    plt.legend(loc='upper left');



.. image:: matplotlib_files/matplotlib_16_0.png


Saving figures
~~~~~~~~~~~~~~

We can save a figure to the disk by calling matplotlib's ``savefig``
function:

.. code:: python

    plt.plot(emissions.index, emissions['Total Emissions'])
    plt.savefig('Figure_1_Total_Emissions.png')



.. image:: matplotlib_files/matplotlib_18_0.png


Matplotlib and Pandas
---------------------

Pandas uses matplot lib to provide a basic plotting interface of its
own. The dataframe we have been working with has a convenience method
called ``.plot()``, which assumes some basic format for how you would
like your data presented, and tries to do so for you.

This is handy when you are just interested in having a quick look at
your data, without going to the trouble to create finished plots.

.. code:: python

    emissions.plot();



.. image:: matplotlib_files/matplotlib_20_0.png


The Dataframe's wrapper of matplotlib gives us a number of basic options
for how our plots are shown:

.. code:: python

    emissions.plot(subplots=True, figsize=(10,6));



.. image:: matplotlib_files/matplotlib_22_0.png


Matplotlib and PySD
-------------------

As PySD returns a Pandas Dataframe, we can either use the plotting
interface directly, or Pandas's convenience wrapper. Here we'll load a
model which produces a chaotic output in three dimensions to use in our
demonstration.

.. code:: python

    import pysd
    model = pysd.read_vensim('../../models/Roessler_Chaos/roessler_chaos.mdl')
    res = model.run()
    res.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>x</th>
          <th>y</th>
          <th>z</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0.00000</th>
          <td>0.500000</td>
          <td>0.500000</td>
          <td>0.400000</td>
        </tr>
        <tr>
          <th>0.03125</th>
          <td>0.471875</td>
          <td>0.518750</td>
          <td>0.341250</td>
        </tr>
        <tr>
          <th>0.06250</th>
          <td>0.445000</td>
          <td>0.536738</td>
          <td>0.291747</td>
        </tr>
        <tr>
          <th>0.09375</th>
          <td>0.419110</td>
          <td>0.553999</td>
          <td>0.250087</td>
        </tr>
        <tr>
          <th>0.12500</th>
          <td>0.393982</td>
          <td>0.570559</td>
          <td>0.215065</td>
        </tr>
      </tbody>
    </table>
    </div>



Plotting vs. time.

.. code:: python

    plt.plot(res.index, res['x'], 'r')
    plt.plot(res.index, res['y'], 'b')
    plt.plot(res.index, res['z'], 'g');



.. image:: matplotlib_files/matplotlib_26_0.png


Plotting variables against one another

.. code:: python

    plt.plot(res['x'], res['y']);



.. image:: matplotlib_files/matplotlib_28_0.png


While so far I have shown mostly basic, 2d plots, we can also call on
`matplotlib's 3d plotting
engine <http://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html#line-plots>`__

.. code:: python

    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    ax.plot(res['x'], res['y'], res['z']);



.. image:: matplotlib_files/matplotlib_30_0.png


Resources
---------

-  `Gallery <http://matplotlib.org/gallery.html>`__ of different
   matplotlib graphics, showing what types of plots are possible.
-  Getting started with matplotlib `video
   series <https://www.youtube.com/watch?v=q7Bo_J8x_dw&list=PLQVvvaa0QuDfefDfXb9Yf0la1fPDKluPF>`__
