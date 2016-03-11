
Nth Order Delay Demo
====================

This is a fun demonstration designed to build intuition around the idea
that balancing feedback loops with delays lead to oscillation. It uses a
vensim model as the 'system' but provides a way for a user to interact
with the simulation in realtime - essentially acting as the controller -
a balancing feedback loop around the model output.

About this Technique
--------------------

This is a way to interact with the models in realtime using your
keyboard.

Ingredients
-----------

The Game
^^^^^^^^

The student is asked to use the 'up' and 'down' arrow keys to bring a
blue line (the system output) to the value of the dashed red line (the
target). However, the inputs from the keyboard go through a delay
process (here using either the 'first order delay' model, or the 'third
order delay' model).

When we run this cell, the student will have 60 seconds to bring the
blue line to the level of the red line.

.. code:: python

    %pylab
    import pysd
    from matplotlib import animation
    import numpy as np



.. parsed-literal::

    Using matplotlib backend: MacOSX
    Populating the interactive namespace from numpy and matplotlib


.. code:: python

    #import the model (need to import each time to reinitialize) 
    #choose one of the following lines:
    #model = pysd.read_vensim('../../models/Basic_Structures/First_Order_Delay.mdl')
    model = pysd.read_vensim('../../models/Basic_Structures/Third_Order_Delay.mdl')
    
    #set the delay time in the model
    model.set_components({'delay':5})
    
    #set the animation parameters
    fps=4
    seconds=60
    dt=1./fps
    
    #set up the figure axes
    fig, ax = plt.subplots()
    ax.set_xlim(0,1)
    ax.set_ylim(-10, 20)
    ax.set_xticks([])
    title = ax.set_title('Time %.02f'%0)
    
    #draw the target line
    ax.plot([0,1], [10,10], 'r--')
    
    #draw the moving line, just for now. We'll change it later
    line, = ax.plot([0,1], [0,0], lw=2)
    
    #set up variables for simulation
    input_val = 1
    model.components.input = lambda: input_val
    
    #capture keyboard input
    def on_key_press(event):
        global input_val
        if event.key == 'up':
            input_val += .25
        elif event.key == 'down':
            input_val -= .25
        sys.stdout.flush()
        
    fig.canvas.mpl_connect('key_press_event', on_key_press)
    
    #make the animation
    def animate(t):
        #run the simulation forward
        time = model.components.t+dt
        stocks = model.run(return_columns=['input', 'delay_buffer_1', 'delay_buffer_2', 'delay_buffer_3', 'output'],
                           return_timestamps=[time], 
                           initial_condition='current', collect=True)
     
        #make changes to the display
        level = stocks['output']
        line.set_data([0,1], [level, level])
        title.set_text('Time %.02f'%time)
        
    # call the animator.  
    anim = animation.FuncAnimation(fig, animate, repeat=False,
                                   frames=seconds*fps, interval=1000./fps, 
                                   blit=False)


.. code:: python

    record = model.get_record()
    record.head()




.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>input</th>
          <th>delay_buffer_1</th>
          <th>delay_buffer_2</th>
          <th>delay_buffer_3</th>
          <th>output</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0.25</th>
          <td> 1</td>
          <td> 0.221199</td>
          <td> 0.026499</td>
          <td> 0.002161</td>
          <td> 0.002161</td>
        </tr>
        <tr>
          <th>0.50</th>
          <td> 1</td>
          <td> 0.393469</td>
          <td> 0.090204</td>
          <td> 0.014388</td>
          <td> 0.014388</td>
        </tr>
        <tr>
          <th>0.75</th>
          <td> 1</td>
          <td> 0.527633</td>
          <td> 0.173359</td>
          <td> 0.040505</td>
          <td> 0.040505</td>
        </tr>
        <tr>
          <th>1.00</th>
          <td> 1</td>
          <td> 0.632121</td>
          <td> 0.264241</td>
          <td> 0.080301</td>
          <td> 0.080301</td>
        </tr>
        <tr>
          <th>1.25</th>
          <td> 1</td>
          <td> 0.713495</td>
          <td> 0.355364</td>
          <td> 0.131532</td>
          <td> 0.131532</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    record.plot();




.. parsed-literal::

    <matplotlib.axes._subplots.AxesSubplot at 0x10f08a250>



Display student input vs model output
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To show how we did, we can plot the input and output over time. Here we
start to see the oscillatory behavior (for higher order and longer
delays)

.. code:: python

    plt.plot(x,input_collector, label='Your Input')
    plt.plot(x,y, label='Model Response')
    plt.legend(loc='lower right')
    plt.xlabel('Time [Seconds]')
    plt.ylabel('Value');




.. parsed-literal::

    <matplotlib.text.Text at 0x108ab4bd0>



Display the value of each of the buffer stocks over time
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If we plot the stock levels over time, we can see (especially for the
third order case) how the delay works to smooth out the input values.

.. code:: python

    import pandas as pd
    delay_stock_values = pd.DataFrame(stocks_collector)
    delay_stock_values.plot()
    plt.xlabel('Time [Seconds]')
    plt.ylabel('Stock Level');




.. parsed-literal::

    <matplotlib.text.Text at 0x108c7c590>



