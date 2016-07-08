
Saving Simulation Results to a Database
=======================================

There are a number of reasons why you might want to save simulation
results to a database:

-  Observing changes in model output over the course of model
   development
-  Cacheing runs of a model to speed later analysis or display,
   especially in large models
-  Creating a traceable record of your work

It's relatively easy to set up a sequel database and commit runs output
to it. This demo uses sqlite, which creates a database in a local file.

.. code:: python

    import sqlite3
    import numpy as np
    import pysd

Ingredients
-----------

Model
^^^^^

We'll use the simple teacup model for this experiment, and we'll ask for
the value at integer times from ``[0..29]``.

.. code:: python

    model = pysd.read_vensim('../../models/Teacup/Teacup.mdl')
    tseries = range(30)

A database
^^^^^^^^^^

In this example, we'll create a database which will be saved in the
working directory as ``example.db``. We populate its columns with two
columns for storing the parameter values that we'll change from run to
run, and then a column for each timestamp value we intend to save:

.. code:: python

    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    
    # Create table
    c.execute('''CREATE TABLE simulations
                 (room_temperature real, init_teacup_temperature real, 
                  %s ) '''%', '.join(['t%i real'%i for i in tseries]));

Parameters
^^^^^^^^^^

We want to save the output of our model when driven with a variety of
parameters. For demonstration, we'll set these randomly:

.. code:: python

    room_temps = np.random.normal(75, 5, 100)
    init_tea_temps = np.random.normal(175, 15, 100)

The Recipe
----------

We're now ready to simulate our model with the various parameters. After
execution, we construct a SQL insert querry containing each of the
returned values, and commit it to the database.

.. code:: python

    
    for room_temp, init_tea_temp in zip(room_temps, init_tea_temps):
        output = model.run(params={'room_temperature':room_temp}, 
                           initial_condition=(0,{'teacup_temperature':init_tea_temp}),
                           return_timestamps=tseries)
        
        c.execute("INSERT INTO simulations VALUES (%i,%i,%s)"%
                  (room_temp, init_tea_temp, ', '.join(output['teacup_temperature'].apply(str))))
    
        conn.commit()


We can see that the result was added properly by fetching a record:

.. code:: python

    c.execute('SELECT * FROM simulations')
    c.fetchone()




.. parsed-literal::

    (76.0,
     164.0,
     164.722280167,
     156.282130733,
     148.64516467,
     141.734949777,
     135.482334802,
     129.824731228,
     124.705520938,
     120.073467412,
     115.882212071,
     112.089807732,
     108.658298586,
     105.55333885,
     102.74385565,
     100.201730758,
     97.9015209724,
     95.8202050685,
     93.9369526016,
     92.232915272,
     90.69103831,
     89.2958904907,
     88.0335085264,
     86.8912580882,
     85.8577072325,
     84.9225116976,
     84.0763117951,
     83.310638529,
     82.6178286757,
     81.9909483832,
     81.4237236618,
     80.9104773994)



Finally, we must remember to close our connection to the database:

.. code:: python

    conn.close()

.. code:: python

    #remove the database file when we are finished with it.
    !rm example.db
