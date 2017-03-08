
Data handling with Pandas
=========================

Pandas is a library optimized for handling one or two dimensional data
sources [1]. One dimensional data is stored in a ``Series`` object, and
two dimensional data is stored in a ``DataFrame`` object.

Loading the library
~~~~~~~~~~~~~~~~~~~

It is customary to give the library a short handle '``pd``\ ' at import
time:

.. code:: python

    import pandas as pd
    pd.options.display.max_rows = 10 #this line aids in displaying the data concisely


.. parsed-literal::

    /Users/houghton/anaconda/lib/python2.7/site-packages/pandas/computation/__init__.py:19: UserWarning: The installed version of numexpr 2.4.4 is not supported in pandas and will be not be used
    
      UserWarning)


Loading data from CSV files
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pandas gives us a comprehensive set of tools for loading data from `a
variety of
sources <http://pandas.pydata.org/pandas-docs/version/0.18.1/io.html>`__,
including CSV, Excel, SQL, JSON, and Stata, amongst others. In this
demonstration, we'll read a comma separated value file of global
emissions data from the year 1751 until 2011.

The ``.read_csv`` `method <>`__ gives us options for how we want to
format the data as we read it in. In reading in our data file, we want
to skip the second row (indexed as ``1``!) and use the column ``Time``
as the index of our resulting ``DataFrame``.

.. code:: python

    emissions = pd.read_csv('../../data/Climate/global_emissions.csv', 
                            skiprows=[1], index_col='Year')
    emissions  # Display the resulting DataFrame in the notebook




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Total carbon emissions from fossil fuel consumption and cement production (million metric tons of C)</th>
          <th>Carbon emissions from gas fuel consumption</th>
          <th>Carbon emissions from liquid fuel consumption</th>
          <th>Carbon emissions from solid fuel consumption</th>
          <th>Carbon emissions from cement production</th>
          <th>Carbon emissions from gas flaring</th>
          <th>Per capita carbon emissions (metric tons of carbon; after 1949 only)</th>
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
        <tr>
          <th>...</th>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th>2007</th>
          <td>8532</td>
          <td>1563</td>
          <td>3080</td>
          <td>3442</td>
          <td>382</td>
          <td>65</td>
          <td>1.28</td>
        </tr>
        <tr>
          <th>2008</th>
          <td>8740</td>
          <td>1625</td>
          <td>3107</td>
          <td>3552</td>
          <td>387</td>
          <td>68</td>
          <td>1.29</td>
        </tr>
        <tr>
          <th>2009</th>
          <td>8700</td>
          <td>1582</td>
          <td>3039</td>
          <td>3604</td>
          <td>412</td>
          <td>63</td>
          <td>1.27</td>
        </tr>
        <tr>
          <th>2010</th>
          <td>9140</td>
          <td>1698</td>
          <td>3100</td>
          <td>3832</td>
          <td>445</td>
          <td>65</td>
          <td>1.32</td>
        </tr>
        <tr>
          <th>2011</th>
          <td>9449</td>
          <td>1760</td>
          <td>3137</td>
          <td>3997</td>
          <td>491</td>
          <td>63</td>
          <td>1.35</td>
        </tr>
      </tbody>
    </table>
    <p>261 rows × 7 columns</p>
    </div>



Selecting rows of data by name
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Both ``DataFrame`` and ``Series`` objects have an ``index`` attribute
which is used to identify their rows. We can access rows of data
according to this index, using the ``.loc[...]`` syntax.

Between the brackets, we can select individual rows:

::

    emissions.loc[1875]

or ranges of dates:

::

    emissions.loc[1908:1920]

or ranges beginning or ending at a specific point:

::

    emissions.loc[1967:]
    emissions.loc[:1805]

Give these a try and become comfortable selecting index ranges.

.. code:: python

    emissions.loc[1985:1987]




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Total carbon emissions from fossil fuel consumption and cement production (million metric tons of C)</th>
          <th>Carbon emissions from gas fuel consumption</th>
          <th>Carbon emissions from liquid fuel consumption</th>
          <th>Carbon emissions from solid fuel consumption</th>
          <th>Carbon emissions from cement production</th>
          <th>Carbon emissions from gas flaring</th>
          <th>Per capita carbon emissions (metric tons of carbon; after 1949 only)</th>
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
          <th>1985</th>
          <td>5438</td>
          <td>835</td>
          <td>2186</td>
          <td>2237</td>
          <td>131</td>
          <td>49</td>
          <td>1.12</td>
        </tr>
        <tr>
          <th>1986</th>
          <td>5606</td>
          <td>830</td>
          <td>2293</td>
          <td>2300</td>
          <td>137</td>
          <td>46</td>
          <td>1.13</td>
        </tr>
        <tr>
          <th>1987</th>
          <td>5750</td>
          <td>892</td>
          <td>2306</td>
          <td>2364</td>
          <td>143</td>
          <td>44</td>
          <td>1.14</td>
        </tr>
      </tbody>
    </table>
    </div>



Selecting rows of data by position
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to selecting by row names, we can select by the row position
using the ``.iloc`` syntax.

This syntax lets us select the first n rows: >\ ``emissions.iloc[:5]``

or, if we wish, the last n, using a minus sign to indicate counting from
the end of the ``DataFrame``:

    \`\`\` emissions.iloc[-5:]

::


    or rows in the middle:
    >```
    emissions.iloc[10:20]

.. code:: python

    emissions.iloc[1:30]




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Total carbon emissions from fossil fuel consumption and cement production (million metric tons of C)</th>
          <th>Carbon emissions from gas fuel consumption</th>
          <th>Carbon emissions from liquid fuel consumption</th>
          <th>Carbon emissions from solid fuel consumption</th>
          <th>Carbon emissions from cement production</th>
          <th>Carbon emissions from gas flaring</th>
          <th>Per capita carbon emissions (metric tons of carbon; after 1949 only)</th>
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
          <th>1756</th>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>1758</th>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>1760</th>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>...</th>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th>1772</th>
          <td>4</td>
          <td>0</td>
          <td>0</td>
          <td>4</td>
          <td>0</td>
          <td>0</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>1774</th>
          <td>4</td>
          <td>0</td>
          <td>0</td>
          <td>4</td>
          <td>0</td>
          <td>0</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>1776</th>
          <td>4</td>
          <td>0</td>
          <td>0</td>
          <td>4</td>
          <td>0</td>
          <td>0</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>1778</th>
          <td>4</td>
          <td>0</td>
          <td>0</td>
          <td>4</td>
          <td>0</td>
          <td>0</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>1780</th>
          <td>4</td>
          <td>0</td>
          <td>0</td>
          <td>4</td>
          <td>0</td>
          <td>0</td>
          <td>NaN</td>
        </tr>
      </tbody>
    </table>
    <p>15 rows × 7 columns</p>
    </div>



Renaming columns
~~~~~~~~~~~~~~~~

The column names given in the CSV file are too long to use conveniently
in dealing with data. We can assign new column names from a list of
strings, that will be applied in order as the new column names:

.. code:: python

    emissions.columns = ['Total Emissions', 'Gas Emissions', 'Liquid Emissions', 
                         'Solid Emissions', 'Cement Emissions', 'Flare Emissions',
                         'Per Capita Emissions']
    emissions.iloc[-3:]




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
          <th>2009</th>
          <td>8700</td>
          <td>1582</td>
          <td>3039</td>
          <td>3604</td>
          <td>412</td>
          <td>63</td>
          <td>1.27</td>
        </tr>
        <tr>
          <th>2010</th>
          <td>9140</td>
          <td>1698</td>
          <td>3100</td>
          <td>3832</td>
          <td>445</td>
          <td>65</td>
          <td>1.32</td>
        </tr>
        <tr>
          <th>2011</th>
          <td>9449</td>
          <td>1760</td>
          <td>3137</td>
          <td>3997</td>
          <td>491</td>
          <td>63</td>
          <td>1.35</td>
        </tr>
      </tbody>
    </table>
    </div>



Accessing specific columns
~~~~~~~~~~~~~~~~~~~~~~~~~~

Each of the columns in the ``DataFrame`` can be accessed as its own
``Series`` object, using the same syntax we would use to access members
of a python dictionary:

.. code:: python

    emissions['Total Emissions']


::


    ---------------------------------------------------------------------------

    KeyError                                  Traceback (most recent call last)

    <ipython-input-9-dc76c55d0847> in <module>()
    ----> 1 emissions[['Total Emissions']]
    

    /Users/houghton/anaconda/lib/python2.7/site-packages/pandas/core/frame.pyc in __getitem__(self, key)
       1984         if isinstance(key, (Series, np.ndarray, Index, list)):
       1985             # either boolean or fancy integer index
    -> 1986             return self._getitem_array(key)
       1987         elif isinstance(key, DataFrame):
       1988             return self._getitem_frame(key)


    /Users/houghton/anaconda/lib/python2.7/site-packages/pandas/core/frame.pyc in _getitem_array(self, key)
       2028             return self.take(indexer, axis=0, convert=False)
       2029         else:
    -> 2030             indexer = self.ix._convert_to_indexer(key, axis=1)
       2031             return self.take(indexer, axis=1, convert=True)
       2032 


    /Users/houghton/anaconda/lib/python2.7/site-packages/pandas/core/indexing.pyc in _convert_to_indexer(self, obj, axis, is_setter)
       1208                 mask = check == -1
       1209                 if mask.any():
    -> 1210                     raise KeyError('%s not in index' % objarr[mask])
       1211 
       1212                 return _values_from_object(indexer)


    KeyError: "['Total Emissions'] not in index"


Passing a list of column names into this syntax returns a subset of the
dataframe:

.. code:: python

    emissions[['Gas Emissions', 'Liquid Emissions']]




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Gas Emissions</th>
          <th>Liquid Emissions</th>
        </tr>
        <tr>
          <th>Year</th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>1751</th>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>1752</th>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>1753</th>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>1754</th>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>1755</th>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>...</th>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th>2007</th>
          <td>1563</td>
          <td>3080</td>
        </tr>
        <tr>
          <th>2008</th>
          <td>1625</td>
          <td>3107</td>
        </tr>
        <tr>
          <th>2009</th>
          <td>1582</td>
          <td>3039</td>
        </tr>
        <tr>
          <th>2010</th>
          <td>1698</td>
          <td>3100</td>
        </tr>
        <tr>
          <th>2011</th>
          <td>1760</td>
          <td>3137</td>
        </tr>
      </tbody>
    </table>
    <p>261 rows × 2 columns</p>
    </div>



Element-wise Arithmetic
~~~~~~~~~~~~~~~~~~~~~~~

We can perform `element-wise
arithmetic <http://pandas.pydata.org/pandas-docs/version/0.18.1/dsintro.html#dataframe-interoperability-with-numpy-functions>`__
on ``DataFrame`` columns using natural syntax.

.. code:: python

    emissions['Gas Emissions'] + emissions['Liquid Emissions']




.. parsed-literal::

    Year
    1751       0
    1752       0
    1753       0
    1754       0
    1755       0
            ... 
    2007    4643
    2008    4732
    2009    4621
    2010    4798
    2011    4897
    dtype: int64



Array Operations
~~~~~~~~~~~~~~~~

A number of simple operations are built into Pandas to facilitate
working with the data. For example, we can show `descriptive
statistics <http://pandas.pydata.org/pandas-docs/version/0.18.1/basics.html#descriptive-statistics>`__
such as the maximum value of each column:

.. code:: python

    print emissions.idxmax(), emissions.max()


.. parsed-literal::

    Total Emissions         2011
    Gas Emissions           2011
    Liquid Emissions        2011
    Solid Emissions         2011
    Cement Emissions        2011
    Flare Emissions         1973
    Per Capita Emissions    2011
    dtype: int64 Total Emissions         9449.00
    Gas Emissions           1760.00
    Liquid Emissions        3137.00
    Solid Emissions         3997.00
    Cement Emissions         491.00
    Flare Emissions          110.00
    Per Capita Emissions       1.35
    dtype: float64


The year `in which this maximum value
occurred <http://pandas.pydata.org/pandas-docs/version/0.18.1/basics.html#index-of-min-max-values>`__:

.. code:: python

    emissions.idxmax()




.. parsed-literal::

    Total Emissions         2011
    Gas Emissions           2011
    Liquid Emissions        2011
    Solid Emissions         2011
    Cement Emissions        2011
    Flare Emissions         1973
    Per Capita Emissions    2011
    dtype: int64



Or the sum of each column:

.. code:: python

    emissions.sum()




.. parsed-literal::

    Total Emissions         373729.0
    Gas Emissions            49774.0
    Liquid Emissions        131976.0
    Solid Emissions         179160.0
    Cement Emissions          9366.0
    Flare Emissions           3456.0
    Per Capita Emissions        65.5
    dtype: float64



.. code:: python

    emissions['Per Capita Emissions'].loc[1930:]




.. parsed-literal::

    Year
    1930     NaN
    1931     NaN
    1932     NaN
    1933     NaN
    1934     NaN
            ... 
    2007    1.28
    2008    1.29
    2009    1.27
    2010    1.32
    2011    1.35
    Name: Per Capita Emissions, dtype: float64



Merging Datasets
~~~~~~~~~~~~~~~~

The dataset we have currently is missing data for per capita consumption
before 1950. We have another dataset which gives us estimates of the
world population which we can use to try and fill in some missing data.
It too, however, has some missing values: before 1900, the data comes at
50 year intervals.

.. code:: python

    population = pd.read_csv('../../data/Climate/world_population.csv', index_col='Year')

What we need to do is first merge the two datasets together. Pandas
gives us a merge function which allows us to align the datasets on their
index values.

.. code:: python

    merged = pd.merge(emissions, population, how='outer', left_index=True, right_index=True)
    merged.loc[1750:2011]




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
          <th>World Population</th>
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
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>1750</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>8.115621e+08</td>
        </tr>
        <tr>
          <th>1751</th>
          <td>3.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>3.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>1752</th>
          <td>3.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>3.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>1753</th>
          <td>3.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>3.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>1754</th>
          <td>3.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>3.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>...</th>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th>2007</th>
          <td>8532.0</td>
          <td>1563.0</td>
          <td>3080.0</td>
          <td>3442.0</td>
          <td>382.0</td>
          <td>65.0</td>
          <td>1.28</td>
          <td>6.681607e+09</td>
        </tr>
        <tr>
          <th>2008</th>
          <td>8740.0</td>
          <td>1625.0</td>
          <td>3107.0</td>
          <td>3552.0</td>
          <td>387.0</td>
          <td>68.0</td>
          <td>1.29</td>
          <td>6.763733e+09</td>
        </tr>
        <tr>
          <th>2009</th>
          <td>8700.0</td>
          <td>1582.0</td>
          <td>3039.0</td>
          <td>3604.0</td>
          <td>412.0</td>
          <td>63.0</td>
          <td>1.27</td>
          <td>6.846480e+09</td>
        </tr>
        <tr>
          <th>2010</th>
          <td>9140.0</td>
          <td>1698.0</td>
          <td>3100.0</td>
          <td>3832.0</td>
          <td>445.0</td>
          <td>65.0</td>
          <td>1.32</td>
          <td>6.929725e+09</td>
        </tr>
        <tr>
          <th>2011</th>
          <td>9449.0</td>
          <td>1760.0</td>
          <td>3137.0</td>
          <td>3997.0</td>
          <td>491.0</td>
          <td>63.0</td>
          <td>1.35</td>
          <td>7.013427e+09</td>
        </tr>
      </tbody>
    </table>
    <p>262 rows × 8 columns</p>
    </div>



Interpolating missing values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The merge operation creates ``NaN`` values in the rows where data is
missing from the world population column. We can fill these using a
cubic spline interpolation from the surrounding points:

.. code:: python

    interpolated = merged.interpolate(method='cubic')
    interpolated.loc[1750:2011]




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
          <th>World Population</th>
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
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>1750</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>8.115621e+08</td>
        </tr>
        <tr>
          <th>1751</th>
          <td>3.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>3.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>NaN</td>
          <td>8.155185e+08</td>
        </tr>
        <tr>
          <th>1752</th>
          <td>3.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>3.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>NaN</td>
          <td>8.194193e+08</td>
        </tr>
        <tr>
          <th>1753</th>
          <td>3.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>3.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>NaN</td>
          <td>8.232672e+08</td>
        </tr>
        <tr>
          <th>1754</th>
          <td>3.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>3.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>NaN</td>
          <td>8.270645e+08</td>
        </tr>
        <tr>
          <th>...</th>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th>2007</th>
          <td>8532.0</td>
          <td>1563.0</td>
          <td>3080.0</td>
          <td>3442.0</td>
          <td>382.0</td>
          <td>65.0</td>
          <td>1.28</td>
          <td>6.681607e+09</td>
        </tr>
        <tr>
          <th>2008</th>
          <td>8740.0</td>
          <td>1625.0</td>
          <td>3107.0</td>
          <td>3552.0</td>
          <td>387.0</td>
          <td>68.0</td>
          <td>1.29</td>
          <td>6.763733e+09</td>
        </tr>
        <tr>
          <th>2009</th>
          <td>8700.0</td>
          <td>1582.0</td>
          <td>3039.0</td>
          <td>3604.0</td>
          <td>412.0</td>
          <td>63.0</td>
          <td>1.27</td>
          <td>6.846480e+09</td>
        </tr>
        <tr>
          <th>2010</th>
          <td>9140.0</td>
          <td>1698.0</td>
          <td>3100.0</td>
          <td>3832.0</td>
          <td>445.0</td>
          <td>65.0</td>
          <td>1.32</td>
          <td>6.929725e+09</td>
        </tr>
        <tr>
          <th>2011</th>
          <td>9449.0</td>
          <td>1760.0</td>
          <td>3137.0</td>
          <td>3997.0</td>
          <td>491.0</td>
          <td>63.0</td>
          <td>1.35</td>
          <td>7.013427e+09</td>
        </tr>
      </tbody>
    </table>
    <p>262 rows × 8 columns</p>
    </div>



Calculating per capita emissions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now we can calculate a new value for per capita emissions. We multiply
by ``1,000,000`` to convert from units of 'Million Metric Tons' as the
Total Emissions are expressed, to merely 'Metric Tons', as the existing,
incomplete estimate of per capita emissions is expressed.

.. code:: python

    interpolated['Per Capita Emissions 2'] = interpolated['Total Emissions'] / interpolated['World Population'] * 1000000
    interpolated.loc[1751:2011]




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
          <th>World Population</th>
          <th>Per Capita Emissions 2</th>
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
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>1751</th>
          <td>3.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>3.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>NaN</td>
          <td>8.155185e+08</td>
          <td>0.003679</td>
        </tr>
        <tr>
          <th>1752</th>
          <td>3.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>3.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>NaN</td>
          <td>8.194193e+08</td>
          <td>0.003661</td>
        </tr>
        <tr>
          <th>1753</th>
          <td>3.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>3.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>NaN</td>
          <td>8.232672e+08</td>
          <td>0.003644</td>
        </tr>
        <tr>
          <th>1754</th>
          <td>3.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>3.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>NaN</td>
          <td>8.270645e+08</td>
          <td>0.003627</td>
        </tr>
        <tr>
          <th>1755</th>
          <td>3.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>3.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>NaN</td>
          <td>8.308138e+08</td>
          <td>0.003611</td>
        </tr>
        <tr>
          <th>...</th>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th>2007</th>
          <td>8532.0</td>
          <td>1563.0</td>
          <td>3080.0</td>
          <td>3442.0</td>
          <td>382.0</td>
          <td>65.0</td>
          <td>1.28</td>
          <td>6.681607e+09</td>
          <td>1.276938</td>
        </tr>
        <tr>
          <th>2008</th>
          <td>8740.0</td>
          <td>1625.0</td>
          <td>3107.0</td>
          <td>3552.0</td>
          <td>387.0</td>
          <td>68.0</td>
          <td>1.29</td>
          <td>6.763733e+09</td>
          <td>1.292186</td>
        </tr>
        <tr>
          <th>2009</th>
          <td>8700.0</td>
          <td>1582.0</td>
          <td>3039.0</td>
          <td>3604.0</td>
          <td>412.0</td>
          <td>63.0</td>
          <td>1.27</td>
          <td>6.846480e+09</td>
          <td>1.270726</td>
        </tr>
        <tr>
          <th>2010</th>
          <td>9140.0</td>
          <td>1698.0</td>
          <td>3100.0</td>
          <td>3832.0</td>
          <td>445.0</td>
          <td>65.0</td>
          <td>1.32</td>
          <td>6.929725e+09</td>
          <td>1.318956</td>
        </tr>
        <tr>
          <th>2011</th>
          <td>9449.0</td>
          <td>1760.0</td>
          <td>3137.0</td>
          <td>3997.0</td>
          <td>491.0</td>
          <td>63.0</td>
          <td>1.35</td>
          <td>7.013427e+09</td>
          <td>1.347273</td>
        </tr>
      </tbody>
    </table>
    <p>261 rows × 9 columns</p>
    </div>



Pandas and PySD
---------------

By default, PySD will return the results of model simulation as a Pandas
``DataFrame``, with the column names representing elements of the model,
and the index (row names) as timestamps in the model.

.. code:: python

    import pysd
    model = pysd.read_vensim('../../models/Predator_Prey/Predator_Prey.mdl')
    sim_result_df = model.run()
    sim_result_df

In this case, may want to downsample the returned data to make it more
manageable:

.. code:: python

    sim_result_df.loc[range(50)]

Notes
~~~~~

[1]: While pandas can handle dimensions larger than two, it is clunky.
`Xarray <http://xarray.pydata.org/en/stable/>`__ is a package for
handling multidimensional data that interfaces well with Pandas.

Resources
~~~~~~~~~

-  `Basic
   introduction <http://pandas.pydata.org/pandas-docs/stable/10min.html>`__
   to Pandas constructs
-  `More
   advanced <http://pandas.pydata.org/pandas-docs/stable/cookbook.html#cookbook>`__
   usage of Pandas syntax
-  `Cookbook of Pandas
   Applications <https://github.com/jvns/pandas-cookbook>`__
