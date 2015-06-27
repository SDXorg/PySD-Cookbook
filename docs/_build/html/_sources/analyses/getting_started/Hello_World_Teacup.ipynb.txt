
Hello World: The Teacup Model
=============================

This notebook demonstrates the basic capability of PySD using a model of
a cup of tea cooling to room temperature.

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
    model = pysd.read_vensim('models/Teacup/Teacup.mdl')
    print model.components.doc()


.. parsed-literal::

    Populating the interactive namespace from numpy and matplotlib
    characteristic_time = 10 
    Type: Flow or Auxiliary 
     
    
    This function returns an aggregation of all of the docstrings of all of the
    elements in the model.
    
    final_time = 30 
    Type: Flow or Auxiliary 
     
    
    heat_loss_to_room = (self.teacup_temperature()- self.room_temperature()) / self.characteristic_time() 
    Type: Flow or Auxiliary 
     
    
    initial_time = 0 
    Type: Flow or Auxiliary 
     
    
    room_temperature = 70 
    Type: Flow or Auxiliary 
     
    
    Stock: teacup_temperature =                      
             -self.heat_loss_to_room()                          
                                         
    Initial Value: 180                    
    Do not overwrite this function       
    
    This helper function allows the model components to
    access the time component directly.
    
    time_step = 0.125 
    Type: Flow or Auxiliary 
     
    
    


Run with default parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To understand the general behavior of the model, we can run a simulation
using the default parameters specified by the Vensim model file. The
default behavior of the run function is to return the value of the
stocks as a `pandas <http://pandas.pydata.org/>`__ dataframe:

.. code:: python

    stocks = model.run()
    stocks.head(5)




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>teacup_temperature</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0.000</th>
          <td>180.000000</td>
        </tr>
        <tr>
          <th>0.125</th>
          <td>178.633556</td>
        </tr>
        <tr>
          <th>0.250</th>
          <td>177.284092</td>
        </tr>
        <tr>
          <th>0.375</th>
          <td>175.951388</td>
        </tr>
        <tr>
          <th>0.500</th>
          <td>174.635239</td>
        </tr>
      </tbody>
    </table>
    </div>



Pandas has some simple plotting utility built in which allows us to
easily visualize the results.

.. code:: python

    plt.figure(figsize(6,2))
    stocks.plot()
    plt.ylabel('Degrees F')
    plt.xlabel('Minutes');



.. parsed-literal::

    <matplotlib.figure.Figure at 0x10d867910>



.. image:: docs/analyses/getting_started/Hello_World_Teacup.ipynb_files/docs/analyses/getting_started/Hello_World_Teacup.ipynb_5_1.png


Return additional model components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If we wish to see the values of model components other than the stocks,
we can pass a list of component names with the keyword argument
``return_columns``. This will change the columns of the returned
dataframe such that they contain samples of the requested model
components:

.. code:: python

    values = model.run(return_columns=['teacup_temperature', 'room_temperature'])
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
          <th>room_temperature</th>
          <th>teacup_temperature</th>
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
          <td>178.633556</td>
        </tr>
        <tr>
          <th>0.250</th>
          <td>70</td>
          <td>177.284092</td>
        </tr>
        <tr>
          <th>0.375</th>
          <td>70</td>
          <td>175.951388</td>
        </tr>
        <tr>
          <th>0.500</th>
          <td>70</td>
          <td>174.635239</td>
        </tr>
      </tbody>
    </table>
    </div>




.. image:: docs/analyses/getting_started/Hello_World_Teacup.ipynb_files/docs/analyses/getting_started/Hello_World_Teacup.ipynb_7_1.png


Return values at a specific time
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes we want to specify the timestamps that the run function should
return values. For instance, if we are comparing the result of our model
with data that arrives at irregular time intervals. We can do so using
the ``return_timestamps`` keyword argument. This argument expects a list
of timestamps, and will return values at those timestamps.

.. code:: python

    stocks = model.run(return_timestamps=[0,1,3,7,9.5, 13.178, 21, 25, 30])
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
          <th>teacup_temperature</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0.0</th>
          <td>180.000000</td>
        </tr>
        <tr>
          <th>1.0</th>
          <td>169.532119</td>
        </tr>
        <tr>
          <th>3.0</th>
          <td>151.490002</td>
        </tr>
        <tr>
          <th>7.0</th>
          <td>124.624385</td>
        </tr>
        <tr>
          <th>9.5</th>
          <td>112.541515</td>
        </tr>
      </tbody>
    </table>
    </div>




.. image:: docs/analyses/getting_started/Hello_World_Teacup.ipynb_files/docs/analyses/getting_started/Hello_World_Teacup.ipynb_9_1.png


Modify parameter values
~~~~~~~~~~~~~~~~~~~~~~~

We can specify changes to the parameters of the model in the call to the
run function. Here we set the room temperature to the constant value of
20 degrees before running the simulation.

.. code:: python

    values = model.run(params={'room_temperature':20})
    values.plot()
    plt.ylabel('Degrees F')
    plt.xlabel('Minutes');



.. image:: docs/analyses/getting_started/Hello_World_Teacup.ipynb_files/docs/analyses/getting_started/Hello_World_Teacup.ipynb_11_0.png


We can also specify that a parameter be set with a time-varying input.
In this case, we raise the room temperature from 20 to 80 degrees over
the course of the 30 minutes. We can see that once the room temperature
rises above that of the tea, the tea begins to warm up again.

.. code:: python

    import pandas as pd
    temp_timeseries = pd.Series(index=range(30), data=range(20,80,2))
    values = model.run(params={'room_temperature':temp_timeseries},return_columns=['teacup_temperature', 'room_temperature'])
    values.plot()
    plt.ylabel('Degrees F')
    plt.xlabel('Minutes');



.. image:: docs/analyses/getting_started/Hello_World_Teacup.ipynb_files/docs/analyses/getting_started/Hello_World_Teacup.ipynb_13_0.png


Specifying model initial conditions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to parameters, we can set the initial conditions for the
model, by passing a tuple to the argument ``initial_condition``. In this
case, the first element of the tuple is the time at which the model
should begin its execution, and the second element of the tuple is a
dictionary containing the values of the stocks at that particular time.

.. code:: python

    stocks = model.run(params={'room_temperature':75},
                       initial_condition=(0, {'teacup_temperature':33}))
    stocks.plot()
    plt.ylabel('Degrees F')
    plt.xlabel('Minutes');



.. image:: docs/analyses/getting_started/Hello_World_Teacup.ipynb_files/docs/analyses/getting_started/Hello_World_Teacup.ipynb_15_0.png


Once a model has been run, we can choose to run it forwards again from
its current state. To do this we specify a new set of timestamps over
which we would like the model to run, and pass the
``intitial_condition`` argument the string ``"current"``.

.. code:: python

    values = model.run(initial_condition='current', return_timestamps=range(31,45))
    values.plot()
    plt.ylabel('Degrees F')
    plt.xlabel('Minutes');



.. image:: docs/analyses/getting_started/Hello_World_Teacup.ipynb_files/docs/analyses/getting_started/Hello_World_Teacup.ipynb_17_0.png


Collecting Results
~~~~~~~~~~~~~~~~~~

To collect all output from a series of run commands into a record, set
the ``collect`` flag to ``True``. We can then access an aggregation of
all runs via the ``.get_record()`` method.

This can be helpful when running the model forwards for a period of
time, then returning control to the user, who will specify changes to
the model, and continue the integration forwards. In this case, we
change the room temperature at 30 minutes, perhaps by taking the tea out
into the cold.

.. code:: python

    stocks0 = model.run(params={'room_temperature':75},
                        return_timestamps=range(0,30), collect=True)
    stocks1 = model.run(params={'room_temperature':25}, initial_condition='current',
                        return_timestamps=range(30,60), collect=True)
    stocks = model.get_record()
    
    stocks.plot()
    plt.ylabel('Degrees F')
    plt.xlabel('Minutes');



.. image:: docs/analyses/getting_started/Hello_World_Teacup.ipynb_files/docs/analyses/getting_started/Hello_World_Teacup.ipynb_19_0.png


To reset the record, use the method ``.clear_record()`` :

.. code:: python

    model.clear_record()
