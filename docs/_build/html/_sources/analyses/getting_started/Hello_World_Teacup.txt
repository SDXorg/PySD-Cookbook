
Hello World: The Teacup Model
=============================

This notebook demonstrates the basic capability of PySD using a model of
a cup of tea cooling to room temperature.

.. image:: ../../../source/models/Teacup/Teacup.png
   :width: 300 px

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
    model = pysd.read_vensim('../../models/Teacup/Teacup.mdl')


.. parsed-literal::

    Populating the interactive namespace from numpy and matplotlib


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
default behavior of the run function is to return the value of all
variables as a `pandas <http://pandas.pydata.org/>`__ dataframe:

.. code:: python

    values = model.run()
    values.head(5)




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Characteristic Time</th>
          <th>FINAL TIME</th>
          <th>Heat Loss to Room</th>
          <th>INITIAL TIME</th>
          <th>Room Temperature</th>
          <th>SAVEPER</th>
          <th>TIME</th>
          <th>TIME STEP</th>
          <th>Teacup Temperature</th>
          <th>Time</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0.000</th>
          <td>10</td>
          <td>30</td>
          <td>11.000000</td>
          <td>0</td>
          <td>70</td>
          <td>0.125</td>
          <td>0.000</td>
          <td>0.125</td>
          <td>180.000000</td>
          <td>0.000</td>
        </tr>
        <tr>
          <th>0.125</th>
          <td>10</td>
          <td>30</td>
          <td>10.862500</td>
          <td>0</td>
          <td>70</td>
          <td>0.125</td>
          <td>0.125</td>
          <td>0.125</td>
          <td>178.625000</td>
          <td>0.125</td>
        </tr>
        <tr>
          <th>0.250</th>
          <td>10</td>
          <td>30</td>
          <td>10.726719</td>
          <td>0</td>
          <td>70</td>
          <td>0.125</td>
          <td>0.250</td>
          <td>0.125</td>
          <td>177.267188</td>
          <td>0.250</td>
        </tr>
        <tr>
          <th>0.375</th>
          <td>10</td>
          <td>30</td>
          <td>10.592635</td>
          <td>0</td>
          <td>70</td>
          <td>0.125</td>
          <td>0.375</td>
          <td>0.125</td>
          <td>175.926348</td>
          <td>0.375</td>
        </tr>
        <tr>
          <th>0.500</th>
          <td>10</td>
          <td>30</td>
          <td>10.460227</td>
          <td>0</td>
          <td>70</td>
          <td>0.125</td>
          <td>0.500</td>
          <td>0.125</td>
          <td>174.602268</td>
          <td>0.500</td>
        </tr>
      </tbody>
    </table>
    </div>



Pandas has some simple plotting utility built in which allows us to
easily visualize the results.

.. code:: python

    values.plot()
    plt.ylabel('Degrees F')
    plt.xlabel('Minutes')
    plt.legend(loc='center left', bbox_to_anchor=(1,.5));



.. image:: Hello_World_Teacup_files/Hello_World_Teacup_8_0.png


Return specific model components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If we wish to see values of only certain variables, we can pass a list
of component names with the keyword argument ``return_columns``. This
will change the columns of the returned dataframe such that they contain
samples of the requested model components. This is (very) slightly
faster, but often cleaner:

.. code:: python

    values = model.run(return_columns=['Teacup Temperature', 'Room Temperature'])
    values.plot()
    plt.ylabel('Degrees F')
    plt.xlabel('Minutes')
    values.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Room Temperature</th>
          <th>Teacup Temperature</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0.000</th>
          <td>70</td>
          <td>180.000000</td>
        </tr>
        <tr>
          <th>0.125</th>
          <td>70</td>
          <td>178.625000</td>
        </tr>
        <tr>
          <th>0.250</th>
          <td>70</td>
          <td>177.267188</td>
        </tr>
        <tr>
          <th>0.375</th>
          <td>70</td>
          <td>175.926348</td>
        </tr>
        <tr>
          <th>0.500</th>
          <td>70</td>
          <td>174.602268</td>
        </tr>
      </tbody>
    </table>
    </div>




.. image:: Hello_World_Teacup_files/Hello_World_Teacup_10_1.png


Return values at a specific time
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes we want to specify the timestamps that the run function should
return values. For instance, if we are comparing the result of our model
with data that arrives at irregular time intervals. We can do so using
the ``return_timestamps`` keyword argument. This argument expects a list
of timestamps, and will return values at those timestamps.

.. code:: python

    stocks = model.run(return_timestamps=[0,1,3,7,9.5, 13.178, 21, 25, 30],
                       return_columns=['Teacup Temperature'])
    stocks.plot(linewidth=0, marker='o')
    plt.ylabel('Degrees F')
    plt.xlabel('Minutes')
    stocks.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Teacup Temperature</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0.0</th>
          <td>180.000000</td>
        </tr>
        <tr>
          <th>1.0</th>
          <td>169.469405</td>
        </tr>
        <tr>
          <th>3.0</th>
          <td>151.336071</td>
        </tr>
        <tr>
          <th>7.0</th>
          <td>124.383922</td>
        </tr>
        <tr>
          <th>9.5</th>
          <td>112.287559</td>
        </tr>
      </tbody>
    </table>
    </div>




.. image:: Hello_World_Teacup_files/Hello_World_Teacup_12_1.png


Modify parameter values
~~~~~~~~~~~~~~~~~~~~~~~

We can specify changes to the parameters of the model in the call to the
run function. Here we set the room temperature to the constant value of
20 degrees before running the simulation.

.. code:: python

    values = model.run(params={'Room Temperature':50}, 
                       return_columns=['Teacup Temperature', 'Room Temperature'])
    values.plot()
    plt.ylabel('Degrees F')
    plt.xlabel('Minutes');



.. image:: Hello_World_Teacup_files/Hello_World_Teacup_14_0.png


We can also specify that a parameter be set with a time-varying input.
In this case, we raise the room temperature from 20 to 80 degrees over
the course of the 30 minutes. We can see that once the room temperature
rises above that of the tea, the tea begins to warm up again.

.. code:: python

    import pandas as pd
    temp_timeseries = pd.Series(index=range(30), data=range(20,80,2))
    values = model.run(params={'Room Temperature':temp_timeseries},
                       return_columns=['Teacup Temperature', 'Room Temperature'])
    values.plot()
    plt.ylabel('Degrees F')
    plt.xlabel('Minutes');



.. image:: Hello_World_Teacup_files/Hello_World_Teacup_16_0.png


Note that when you set a variable equal to a value, you overwrite the
existing formula for that variable. This means that if you assign a
value to a variable which is computed based upon other variable values,
you will break those links in the causal structure. This can be helpful
when you wish to isolate part of a model structure, or perform
loop-knockout analysis, but can also lead to mistakes. To return to the
original model structure, you'll need to reload the model.

Specifying model initial conditions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to parameters, we can set the initial conditions for the
model, by passing a tuple to the argument ``initial_condition``. In this
case, the first element of the tuple is the time at which the model
should begin its execution, and the second element of the tuple is a
dictionary containing the values of the stocks at that particular time.

Note again that this is a different syntax from merely sending a new
value to the stock using the ``params`` syntax, which could cause
unintended behavior as previously described.

.. code:: python

    stocks = model.run(params={'room_temperature':75},
                       initial_condition=(0, {'teacup_temperature':33}),
                       return_columns=['Teacup Temperature', 'Room Temperature'])
    stocks.plot()
    plt.ylabel('Degrees F')
    plt.ylim(30,80)
    plt.xlabel('Minutes');



.. image:: Hello_World_Teacup_files/Hello_World_Teacup_19_0.png


Once a model has been run, we can choose to run it forwards again from
its current state. To do this we specify a new set of timestamps over
which we would like the model to run, and pass the
``intitial_condition`` argument the string ``"current"``.

.. code:: python

    values = model.run(initial_condition='current', 
                       return_columns=['Teacup Temperature', 'Room Temperature'],
                       return_timestamps=list(range(31,45)))
    values.plot()
    plt.ylabel('Degrees F')
    plt.ylim(30,80)
    plt.xlabel('Minutes');



.. image:: Hello_World_Teacup_files/Hello_World_Teacup_21_0.png

