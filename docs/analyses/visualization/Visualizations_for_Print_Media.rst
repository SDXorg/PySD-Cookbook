
Visualizations for Print Media
==============================

There are a wealth of python libraries that make creating beautiful
figures for print (in color and b/w) extremely easy. In this notebook,
we'll cover a few of the most common applications of data visualization
in system dynamics.

Contents:
^^^^^^^^^

-  Plotting model outputs
-  single axis
-  multiple axis
-  left and right scales

-  Illustrating uncertainty
-  Monte carlo

Other resources
^^^^^^^^^^^^^^^

For a more thorough treatment of visualization techniques using python
tools, see

.. code:: python

    %pylab inline
    #import seaborn
    import pysd
    import numpy as np
    import pandas as pd


.. parsed-literal::

    Populating the interactive namespace from numpy and matplotlib


.. code:: python

    model = pysd.read_vensim('../../models/Teacup/Teacup.mdl')

.. code:: python

    model.run().plot();
    plt.xlabel('Time')
    plt.ylabel('Temperature [$^\circ F$]')
    plt.title('Visualizing the Cooling of a Cup of Tea');



.. image:: Visualizations_for_Print_Media_files/Visualizations_for_Print_Media_3_0.png


Uncertainty:
~~~~~~~~~~~~

.. code:: python

    results = []
    for i in range(1000):
        results.append(model.run(params={'characteristic_time':np.random.normal(15,3)})['teacup_temperature'])
    
    resultsdf = pd.DataFrame(results)
    resultsdf.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>0.0</th>
          <th>0.125</th>
          <th>0.25</th>
          <th>0.375</th>
          <th>0.5</th>
          <th>0.625</th>
          <th>0.75</th>
          <th>0.875</th>
          <th>1.0</th>
          <th>1.125</th>
          <th>...</th>
          <th>28.75</th>
          <th>28.875</th>
          <th>29.0</th>
          <th>29.125</th>
          <th>29.25</th>
          <th>29.375</th>
          <th>29.5</th>
          <th>29.625</th>
          <th>29.75</th>
          <th>29.875</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>teacup_temperature</th>
          <td>180</td>
          <td>178.834702</td>
          <td>177.681751</td>
          <td>176.541015</td>
          <td>175.412362</td>
          <td>174.295665</td>
          <td>173.190798</td>
          <td>172.097635</td>
          <td>171.016053</td>
          <td>169.945928</td>
          <td>...</td>
          <td>79.496782</td>
          <td>79.396176</td>
          <td>79.296637</td>
          <td>79.198152</td>
          <td>79.100710</td>
          <td>79.004301</td>
          <td>78.908913</td>
          <td>78.814536</td>
          <td>78.721158</td>
          <td>78.628769</td>
        </tr>
        <tr>
          <th>teacup_temperature</th>
          <td>180</td>
          <td>179.130432</td>
          <td>178.267738</td>
          <td>177.411869</td>
          <td>176.562764</td>
          <td>175.720369</td>
          <td>174.884634</td>
          <td>174.055505</td>
          <td>173.232931</td>
          <td>172.416859</td>
          <td>...</td>
          <td>87.726688</td>
          <td>87.586556</td>
          <td>87.447531</td>
          <td>87.309606</td>
          <td>87.172771</td>
          <td>87.037017</td>
          <td>86.902337</td>
          <td>86.768722</td>
          <td>86.636162</td>
          <td>86.504651</td>
        </tr>
        <tr>
          <th>teacup_temperature</th>
          <td>180</td>
          <td>179.367218</td>
          <td>178.738076</td>
          <td>178.112553</td>
          <td>177.490632</td>
          <td>176.872288</td>
          <td>176.257499</td>
          <td>175.646247</td>
          <td>175.038511</td>
          <td>174.434271</td>
          <td>...</td>
          <td>99.182583</td>
          <td>99.014709</td>
          <td>98.847800</td>
          <td>98.681851</td>
          <td>98.516857</td>
          <td>98.352812</td>
          <td>98.189711</td>
          <td>98.027548</td>
          <td>97.866318</td>
          <td>97.706016</td>
        </tr>
        <tr>
          <th>teacup_temperature</th>
          <td>180</td>
          <td>178.963633</td>
          <td>177.937029</td>
          <td>176.920103</td>
          <td>175.912753</td>
          <td>174.914895</td>
          <td>173.926438</td>
          <td>172.947293</td>
          <td>171.977374</td>
          <td>171.016593</td>
          <td>...</td>
          <td>82.469171</td>
          <td>82.351692</td>
          <td>82.235320</td>
          <td>82.120045</td>
          <td>82.005856</td>
          <td>81.892743</td>
          <td>81.780695</td>
          <td>81.669703</td>
          <td>81.559757</td>
          <td>81.450846</td>
        </tr>
        <tr>
          <th>teacup_temperature</th>
          <td>180</td>
          <td>179.074919</td>
          <td>178.157620</td>
          <td>177.248038</td>
          <td>176.346104</td>
          <td>175.451754</td>
          <td>174.564925</td>
          <td>173.685554</td>
          <td>172.813578</td>
          <td>171.948936</td>
          <td>...</td>
          <td>85.768987</td>
          <td>85.636373</td>
          <td>85.504874</td>
          <td>85.374481</td>
          <td>85.245185</td>
          <td>85.116976</td>
          <td>84.989845</td>
          <td>84.863783</td>
          <td>84.738782</td>
          <td>84.614831</td>
        </tr>
      </tbody>
    </table>
    <p>5 rows × 240 columns</p>
    </div>



.. code:: python

    for i, row in resultsdf.iterrows():
        plt.plot(row.index, row.values, 'b', alpha=.02)



.. image:: Visualizations_for_Print_Media_files/Visualizations_for_Print_Media_6_0.png


.. code:: python

    import seaborn
    model.run().plot();
    plt.xlabel('Time')
    plt.ylabel('Temperature [$^\circ F$]')
    plt.title('Visualizing the Cooling of a Cup of Tea');



.. image:: Visualizations_for_Print_Media_files/Visualizations_for_Print_Media_7_0.png


