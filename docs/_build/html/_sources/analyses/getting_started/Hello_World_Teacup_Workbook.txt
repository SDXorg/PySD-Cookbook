
Hello World: The Teacup Model
=============================

This notebook demonstrates the basic capability of PySD using a model of
a cup of tea cooling to room temperature.

This workbook is intended to help students follow along with a
demonstration. Though this file you will find code snippets with pieces
missing, the gaps marked with ``<<??>>``. Fill in the gaps by following
along with the instructor, or consulting the base version of this
notebook in which the segments are filled.

Our model simulates `Newton's Law of
Cooling <http://www.ugrad.math.ubc.ca/coursedoc/math100/notes/diffeqs/cool.html>`__,
which follows the functional form:

.. math:: \frac{dT}{dt} = k(T - T_{ambient})

This model has all of the canonical components of a system dynamics
model: a stock, a flow, a feedback loop, a control parameter, and
exhibits dynamic behavior. The model equations are:

::

    Characteristic Time=
            10
    Units: Minutes

    Heat Loss to Room=
        (Teacup Temperature - Room Temperature) / Characteristic Time
    Units: Degrees/Minute
    This is the rate at which heat flows from the cup into the room. 

    Room Temperature=
        70
    Units: Degrees

    Teacup Temperature= INTEG (
        -Heat Loss to Room,
            180)
    Units: Degrees

Load the model
~~~~~~~~~~~~~~

We begin by importing the PySD module using the python standard import
commands. We then use PySD's Vensim model translator to import the model
from the Vensim model file and create a model object. We see that PySD
translates the vensim component names into acceptable python
identifiers.

.. code:: python

    %pylab inline
    import pysd

.. code:: python

    model = pysd.read_vensim('../../models/Teacup/<<??>>')

The ``read_vensim`` command we have just run does two things. First it
translates the model into a python module which is stored
``../../models/Teacup/Teacup.py`` in the same directory as the original
file, with the filename changed to ``.py``. You can go and have a look
at the file and compare it to the vensim model file that it came from to
get a sense for how the translation works.

The second thing the function does is load that translated python file
into a PySD object and return it for use.

Run with default parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To understand the general behavior of the model, we can run a simulation
using the default parameters specified by the Vensim model file. The
default behavior of the run function is to return the value of the
stocks as a `pandas <http://pandas.pydata.org/>`__ dataframe:

.. code:: python

    stocks = model.<<??>>
    stocks.head(5)

Pandas has some simple plotting utility built in which allows us to
easily visualize the results.

.. code:: python

    plt.figure(figsize(6,2))
    stocks.<<??>>
    plt.ylabel('Degrees F')
    plt.xlabel('Minutes');

Return additional model components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If we wish to see the values of model components other than the stocks,
we can pass a list of component names with the keyword argument
``return_columns``. This will change the columns of the returned
dataframe such that they contain samples of the requested model
components:

.. code:: python

    values = model.run(<<??>>=['teacup_temperature', 'room_temperature'])
    values.plot()
    plt.ylabel('Degrees F')
    plt.xlabel('Minutes') 
    values.head()

Return values at a specific time
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes we want to specify the timestamps that the run function should
return values. For instance, if we are comparing the result of our model
with data that arrives at irregular time intervals. We can do so using
the ``return_timestamps`` keyword argument. This argument expects a list
of timestamps, and will return values at those timestamps.

.. code:: python

    stocks = model.run(<<??>>=[0,1,3,7,14.87456,30])
    stocks.plot(linewidth=0, marker='o')
    plt.ylabel('Degrees F')
    plt.xlabel('Minutes')
    stocks.head()

Modify parameter values
~~~~~~~~~~~~~~~~~~~~~~~

We can specify changes to the parameters of the model in the call to the
run function. Here we set the room temperature to the constant value of
20 degrees before running the simulation.

.. code:: python

    values = model.run(params={<<??>>:22})
    values.plot()
    plt.ylabel('Degrees F')
    plt.xlabel('Minutes');

We can also specify that a parameter be set with a time-varying input.
In this case, we raise the room temperature from 20 to 80 degrees over
the course of the 30 minutes. We can see that once the room temperature
rises above that of the tea, the tea begins to warm up again.

.. code:: python

    import pandas as pd
    temp_timeseries = pd.Series(index=range(30), data=range(20,80,2))
    values = model.run(params={'room_temperature':<<??>>},
                       return_columns=['teacup_temperature', 'room_temperature'])
    values.plot()
    plt.ylabel('Degrees F')
    plt.xlabel('Minutes');

Specifying model initial conditions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to parameters, we can set the initial conditions for the
model, by passing a tuple to the argument ``initial_condition``. In this
case, the first element of the tuple is the time at which the model
should begin its execution, and the second element of the tuple is a
dictionary containing the values of the stocks at that particular time.

.. code:: python

    stocks = model.run(params={'room_temperature':75},
                       <<??>>=(0, {'teacup_temperature':30}))
    stocks.plot()
    plt.ylabel('Degrees F')
    plt.xlabel('Minutes');

