
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

    emissions = pd.<<...>>('../../data/Climate/global_emissions.csv',  # add the call to `read_csv`
                            skiprows=[1], index_col='Year')
    emissions  # Display the resulting DataFrame in the notebook

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

    emissions.loc[<<...>>] # try some of the values above, or some of your own

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

    emissions.iloc[<<...>>]  # Try some of the values above

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

Accessing specific columns
~~~~~~~~~~~~~~~~~~~~~~~~~~

Each of the columns in the ``DataFrame`` can be accessed as its own
``Series`` object, using the same syntax we would use to access members
of a python dictionary:

.. code:: python

    emissions['<<...>>']  # Choose one of the columns using its name

Passing a list of column names into this syntax returns a subset of the
dataframe:

.. code:: python

    emissions[['Gas Emissions', 'Liquid Emissions']]

Element-wise Arithmetic
~~~~~~~~~~~~~~~~~~~~~~~

We can perform `element-wise
arithmetic <http://pandas.pydata.org/pandas-docs/version/0.18.1/dsintro.html#dataframe-interoperability-with-numpy-functions>`__
on ``DataFrame`` columns using natural syntax.

.. code:: python

    emissions['Gas Emissions'] <<...>> emissions['Liquid Emissions'] # try using a '+' or '-' operator

Array Operations
~~~~~~~~~~~~~~~~

A number of simple operations are built into Pandas to facilitate
working with the data. For example, we can show `descriptive
statistics <http://pandas.pydata.org/pandas-docs/version/0.18.1/basics.html#descriptive-statistics>`__
such as the maximum value of each column:

.. code:: python

    emissions.max()

The year `in which this maximum value
occurred <http://pandas.pydata.org/pandas-docs/version/0.18.1/basics.html#index-of-min-max-values>`__:

.. code:: python

    emissions.idxmax()

Or the sum of each column:

.. code:: python

    emissions.<<...>>() # substitute the function name 'sum'

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

    # substitute 'outer' for the value of how
    merged = pd.merge(emissions, population, how='<<...>>', left_index=True, right_index=True)  
    merged.loc[1750:2011]

Interpolating missing values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The merge operation creates ``NaN`` values in the rows where data is
missing from the world population column. We can fill these using a
cubic spline interpolation from the surrounding points:

.. code:: python

    interpolated = merged.interpolate(method='cubic')
    interpolated.loc[1750:2011]

Calculating per capita emissions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now we can calculate a new value for per capita emissions. We multiply
by ``1,000,000`` to convert from units of 'Million Metric Tons' as the
Total Emissions are expressed, to merely 'Metric Tons', as the existing,
incomplete estimate of per capita emissions is expressed.

.. code:: python

    interpolated['Per Capita Emissions 2'] = interpolated['Total Emissions'] / interpolated['World Population'] * 1000000
    interpolated.loc[1751:2011]

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
