
Using SD models to understand the differences between population measures at varying levels of geographic disagregation
=======================================================================================================================

In this recipe, we will use data at a national level to infer parameters
for a population aging model. We'll then try two different ways of using
this trained model to understand variation between the behavior of each
of the states.

About this technique
--------------------

Firstly, we'll use the parameters fit at the national level to predict
census data at the disaggregated level, and compare these predicted
state-level outputs with the measured values. This gives us a sense for
how different the populations of the states are from what we should
expect given our understanding of the national picture.

Secondly, we'll fit parameters to a model at each of the state levels
actual measured census data, and then compare the differences in fit
parameters to each other and to the national expectation. This is a
helpful analysis if the parameter itself (and its inter-state variance)
is what we find interesting.

.. code:: python

    %pylab inline
    import pandas as pd
    import pysd
    import scipy.optimize
    import geopandas as gpd


.. parsed-literal::

    Populating the interactive namespace from numpy and matplotlib


Ingredients
-----------

Population data by age cohort
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We start with data from the decennial census years 2000 and 2010, for
the male population by state and county. We have aggregated the data
into ten-year age cohorts (with the last cohort representing everyone
over 80 years old). The data collection task is described
`here <data/Census/US%20Census%20Data%20Collection.ipynb>`__. In this
analysis we will only use data at the state and national levels.

.. code:: python

    data = pd.read_csv('../../data/Census/Males by decade and county.csv', header=[0,1], index_col=[0,1])
    data.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr>
          <th></th>
          <th></th>
          <th colspan="9" halign="left">2000</th>
          <th colspan="9" halign="left">2010</th>
        </tr>
        <tr>
          <th></th>
          <th></th>
          <th>dec_1</th>
          <th>dec_2</th>
          <th>dec_3</th>
          <th>dec_4</th>
          <th>dec_5</th>
          <th>dec_6</th>
          <th>dec_7</th>
          <th>dec_8</th>
          <th>dec_9</th>
          <th>dec_1</th>
          <th>dec_2</th>
          <th>dec_3</th>
          <th>dec_4</th>
          <th>dec_5</th>
          <th>dec_6</th>
          <th>dec_7</th>
          <th>dec_8</th>
          <th>dec_9</th>
        </tr>
        <tr>
          <th>state</th>
          <th>county</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
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
          <th rowspan="5" valign="top">1</th>
          <th>1</th>
          <td>3375</td>
          <td>3630</td>
          <td>2461</td>
          <td>3407</td>
          <td>3283</td>
          <td>2319</td>
          <td>1637</td>
          <td>825</td>
          <td>284</td>
          <td>3867</td>
          <td>4384</td>
          <td>3082</td>
          <td>3598</td>
          <td>4148</td>
          <td>3390</td>
          <td>2293</td>
          <td>1353</td>
          <td>454</td>
        </tr>
        <tr>
          <th>3</th>
          <td>9323</td>
          <td>10094</td>
          <td>7600</td>
          <td>9725</td>
          <td>10379</td>
          <td>8519</td>
          <td>6675</td>
          <td>4711</td>
          <td>1822</td>
          <td>11446</td>
          <td>12006</td>
          <td>9976</td>
          <td>11042</td>
          <td>12517</td>
          <td>12368</td>
          <td>10623</td>
          <td>6307</td>
          <td>2911</td>
        </tr>
        <tr>
          <th>5</th>
          <td>2002</td>
          <td>2198</td>
          <td>2412</td>
          <td>2465</td>
          <td>2178</td>
          <td>1699</td>
          <td>1026</td>
          <td>689</td>
          <td>301</td>
          <td>1673</td>
          <td>1739</td>
          <td>2260</td>
          <td>2208</td>
          <td>2233</td>
          <td>1910</td>
          <td>1490</td>
          <td>739</td>
          <td>324</td>
        </tr>
        <tr>
          <th>7</th>
          <td>1546</td>
          <td>1460</td>
          <td>1680</td>
          <td>1762</td>
          <td>1624</td>
          <td>1237</td>
          <td>774</td>
          <td>475</td>
          <td>187</td>
          <td>1471</td>
          <td>1577</td>
          <td>1798</td>
          <td>2016</td>
          <td>1928</td>
          <td>1581</td>
          <td>1140</td>
          <td>579</td>
          <td>211</td>
        </tr>
        <tr>
          <th>9</th>
          <td>3741</td>
          <td>3615</td>
          <td>3393</td>
          <td>3901</td>
          <td>3773</td>
          <td>3007</td>
          <td>2227</td>
          <td>1269</td>
          <td>550</td>
          <td>3741</td>
          <td>4252</td>
          <td>3312</td>
          <td>3719</td>
          <td>4129</td>
          <td>3782</td>
          <td>3052</td>
          <td>1723</td>
          <td>652</td>
        </tr>
      </tbody>
    </table>
    </div>



A model of an aging population
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The model we'll use to represent the population is a simple aging chain,
with individuals aggregated into stocks by decade, to match the
agregation we used for the above data. Each cohort is promoted with a
timescale of 10 years, and there is some net inmigration, outmigration,
and death subsumed into the ``loss`` flow associated with each cohort.
This loss is controled by some yearly fraction that it will be our task
to understand.

.. image:: ../../../source/models/Aging_Chain/Aging_Chain.png
   :width: 600 px

.. code:: python

    model = pysd.read_vensim('../../models/Aging_Chain/Aging_Chain.mdl')

Our model is initialy parameterized with 10 individuals in each stock,
no births, and a uniform loss rate of 5%. We'll use data to set the
initial conditions, and infer the loss rates. Estimating births is
difficult, and so for this analysis, we'll pay attention only to
individuals who have been born before the year 2000.

.. code:: python

    model.run().plot();



.. image:: Exploring_models_across_geographic_scales_files/Exploring_models_across_geographic_scales_8_0.png


Geography Information
~~~~~~~~~~~~~~~~~~~~~

This information comes to us as a shape file ``.shp`` with its
associated ``.dbf`` and ``.shx`` conspirator files. Lets check the
plotting functionality:

.. code:: python

    state_geo = gpd.read_file('../../data/Census/US_State.shp')
    state_geo.set_index('StateFIPSN', inplace=True)
    state_geo.plot();
    state_geo.head(2)




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>CensusDiv</th>
          <th>CensusReg</th>
          <th>FIPS</th>
          <th>FIPSNum</th>
          <th>Notes</th>
          <th>OBJECTID</th>
          <th>StateFIPS</th>
          <th>StateName</th>
          <th>XCentroid</th>
          <th>YCentroid</th>
          <th>geometry</th>
        </tr>
        <tr>
          <th>StateFIPSN</th>
          <th></th>
          <th></th>
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
          <th>2</th>
          <td>Pacific</td>
          <td>West</td>
          <td>02000</td>
          <td>2000</td>
          <td>None</td>
          <td>1</td>
          <td>02</td>
          <td>Alaska</td>
          <td>-1882092.15195</td>
          <td>2310348.392810</td>
          <td>(POLYGON ((-2247528.774479387 2237995.01157197...</td>
        </tr>
        <tr>
          <th>53</th>
          <td>Pacific</td>
          <td>West</td>
          <td>53000</td>
          <td>53000</td>
          <td>None</td>
          <td>9</td>
          <td>53</td>
          <td>Washington</td>
          <td>-1837353.15317</td>
          <td>1340481.223852</td>
          <td>(POLYGON ((-2124362.24278068 1480441.850674443...</td>
        </tr>
      </tbody>
    </table>
    </div>




.. image:: Exploring_models_across_geographic_scales_files/Exploring_models_across_geographic_scales_10_1.png


Recipe Part A: Predict state-level values from national model fit
-----------------------------------------------------------------

Step 1: Initialize the model using census data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We can aggregate the county level data to the national scale by summing
across all geographies. This is relatively straightforward.

.. code:: python

    country = data.sum()
    country




.. parsed-literal::

    2000  dec_1    20332536
          dec_2    20909490
          dec_3    19485544
          dec_4    21638975
          dec_5    21016627
          dec_6    15115009
          dec_7     9536197
          dec_8     6946906
          dec_9     3060483
    2010  dec_1    20703935
          dec_2    21878666
          dec_3    21645336
          dec_4    20033352
          dec_5    21597437
          dec_6    20451686
          dec_7    13926846
          dec_8     7424945
          dec_9     4083435
    dtype: float64



If we run the model using national data from the year 2000 as starting
conditions, we can see how the cohorts develop, given our arbitrary loss
rate values:

.. code:: python

    model.run(return_timestamps=range(2000,2011), 
              initial_condition=(2000, country['2000'])).plot();



.. image:: Exploring_models_across_geographic_scales_files/Exploring_models_across_geographic_scales_14_0.png


Step 2: Fit the national level model to the remaining data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We've used half of our data (from the year 2000 census) to initialize
our model. Now we'll use an optimization routine to choose the loss rate
parameters that best predict the census 2010 data. We'll use the same
basic operations described in the previous recipe: `Fitting with
Optimization <2_1_Fitting_with_Optimization.ipynb>`__.

To make this simple, we'll write a function that takes a list of
potential model parameters, and returns the model's prediction in the
year 2010

.. code:: python

    def exec_model(paramlist):
        params = dict(zip(['dec_%i_loss_rate'%i for i in range(1,10)], paramlist)) 
        output = model.run(initial_condition=(2000,country['2000']),
                           params=params, return_timestamps=2010)
        return output

Now we'll define an error function that calls this executor and
calculates a sum of squared errors value. Remember that because we don't
have birth information, we'll only calculate error based upon age
cohorts 2 through 9.

.. code:: python

    def error(paramlist):
        output = exec_model(paramlist)
        errors = output - country['2010']
        #don't tally errors in the first cohort, as we don't have info about births
        return sum(errors.values[0,1:]**2)

Now we can use the minimize function from scipy to find a vector of
parameters which brings the 2010 predictions into alignment with the
data.

.. code:: python

    res = scipy.optimize.minimize(error, x0=[.05]*9,
                                  method='L-BFGS-B')
    country_level_fit_params = dict(zip(['dec_%i_loss_rate'%i for i in range(1,10)], res['x']))
    country_level_fit_params




.. parsed-literal::

    {'dec_1_loss_rate': 0.021183432598200467,
     'dec_2_loss_rate': -0.052101419562612286,
     'dec_3_loss_rate': -0.0014091019293939956,
     'dec_4_loss_rate': 0.0088436979759478375,
     'dec_5_loss_rate': -0.0072046351581388701,
     'dec_6_loss_rate': -0.011046250905098235,
     'dec_7_loss_rate': 0.017228650364514753,
     'dec_8_loss_rate': 0.063195268137886118,
     'dec_9_loss_rate': 0.16077452197707129}



If we run the national model forwards with these parameters, we see
generally good behavior, except for the 0-9yr demographic bracket, from
whom we expect less self-control. (And because we don't have births
data.)

.. code:: python

    model.run(params=country_level_fit_params,
              return_timestamps=range(2000,2011), 
              initial_condition=(2000, country['2000'])).plot();



.. image:: Exploring_models_across_geographic_scales_files/Exploring_models_across_geographic_scales_22_0.png


Step 3: Make state-level predictions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If we want to look at the variances between the states and the national
level, we can try making state-level predictions using state-specific
initial conditions, but parameters fit at the national level.

.. code:: python

    states = data.sum(level=0)
    states.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr>
          <th></th>
          <th colspan="9" halign="left">2000</th>
          <th colspan="9" halign="left">2010</th>
        </tr>
        <tr>
          <th></th>
          <th>dec_1</th>
          <th>dec_2</th>
          <th>dec_3</th>
          <th>dec_4</th>
          <th>dec_5</th>
          <th>dec_6</th>
          <th>dec_7</th>
          <th>dec_8</th>
          <th>dec_9</th>
          <th>dec_1</th>
          <th>dec_2</th>
          <th>dec_3</th>
          <th>dec_4</th>
          <th>dec_5</th>
          <th>dec_6</th>
          <th>dec_7</th>
          <th>dec_8</th>
          <th>dec_9</th>
        </tr>
        <tr>
          <th>state</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
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
          <th>1</th>
          <td>312841</td>
          <td>329043</td>
          <td>301076</td>
          <td>315262</td>
          <td>321447</td>
          <td>246427</td>
          <td>165327</td>
          <td>109918</td>
          <td>45131</td>
          <td>312605</td>
          <td>338568</td>
          <td>321236</td>
          <td>297502</td>
          <td>321810</td>
          <td>318358</td>
          <td>229496</td>
          <td>124070</td>
          <td>56543</td>
        </tr>
        <tr>
          <th>2</th>
          <td>50687</td>
          <td>53992</td>
          <td>42537</td>
          <td>51442</td>
          <td>56047</td>
          <td>35804</td>
          <td>14974</td>
          <td>7628</td>
          <td>2325</td>
          <td>53034</td>
          <td>52278</td>
          <td>58166</td>
          <td>47753</td>
          <td>51856</td>
          <td>54170</td>
          <td>29869</td>
          <td>10392</td>
          <td>4151</td>
        </tr>
        <tr>
          <th>4</th>
          <td>395110</td>
          <td>384672</td>
          <td>386486</td>
          <td>391330</td>
          <td>352471</td>
          <td>257798</td>
          <td>187193</td>
          <td>144837</td>
          <td>61148</td>
          <td>463808</td>
          <td>466275</td>
          <td>455170</td>
          <td>422447</td>
          <td>418398</td>
          <td>381076</td>
          <td>300553</td>
          <td>178849</td>
          <td>89247</td>
        </tr>
        <tr>
          <th>5</th>
          <td>188589</td>
          <td>201405</td>
          <td>180801</td>
          <td>187516</td>
          <td>186931</td>
          <td>149142</td>
          <td>104621</td>
          <td>72629</td>
          <td>33050</td>
          <td>201821</td>
          <td>205074</td>
          <td>196956</td>
          <td>183761</td>
          <td>192596</td>
          <td>188081</td>
          <td>143285</td>
          <td>81138</td>
          <td>38925</td>
        </tr>
        <tr>
          <th>6</th>
          <td>2669364</td>
          <td>2588761</td>
          <td>2556975</td>
          <td>2812648</td>
          <td>2495158</td>
          <td>1692007</td>
          <td>1002881</td>
          <td>725610</td>
          <td>331342</td>
          <td>2573619</td>
          <td>2780997</td>
          <td>2849483</td>
          <td>2595717</td>
          <td>2655307</td>
          <td>2336519</td>
          <td>1489395</td>
          <td>780576</td>
          <td>456217</td>
        </tr>
      </tbody>
    </table>
    </div>



We can now generate a prediction by setting the model's intitial
conditions with state level data, and parameters fit in the national
case. I've created a ``model_runner`` helper function to make the code
easier to read, but this could be conducted in a single line if we so
chose.

.. code:: python

    def model_runner(row):
        result = model.run(params=country_level_fit_params, 
                           initial_condition=(2000,row['2000']), 
                           return_timestamps=2010)
        return result.loc[2010]
        
    state_predictions = states.apply(model_runner, axis=1)
    state_predictions.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>dec_1</th>
          <th>dec_2</th>
          <th>dec_3</th>
          <th>dec_4</th>
          <th>dec_5</th>
          <th>dec_6</th>
          <th>dec_7</th>
          <th>dec_8</th>
          <th>dec_9</th>
        </tr>
        <tr>
          <th>state</th>
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
          <th>1</th>
          <td>93117.371881</td>
          <td>341167.213342</td>
          <td>337071.875334</td>
          <td>304311.201330</td>
          <td>325833.277920</td>
          <td>316445.464900</td>
          <td>223627.149408</td>
          <td>121168.476612</td>
          <td>65739.525962</td>
        </tr>
        <tr>
          <th>2</th>
          <td>15087.025659</td>
          <td>55697.612356</td>
          <td>52613.730625</td>
          <td>47359.482364</td>
          <td>53391.883377</td>
          <td>50862.893499</td>
          <td>31762.129879</td>
          <td>14297.875847</td>
          <td>6133.949764</td>
        </tr>
        <tr>
          <th>4</th>
          <td>117604.805785</td>
          <td>411745.021973</td>
          <td>413024.709292</td>
          <td>377589.072369</td>
          <td>386843.833461</td>
          <td>354697.832262</td>
          <td>246306.408711</td>
          <td>138031.543558</td>
          <td>79499.152922</td>
        </tr>
        <tr>
          <th>5</th>
          <td>56133.665931</td>
          <td>207553.388634</td>
          <td>204417.938099</td>
          <td>183004.303895</td>
          <td>192875.524445</td>
          <td>187772.888790</td>
          <td>135135.556656</td>
          <td>75209.777699</td>
          <td>42570.643627</td>
        </tr>
        <tr>
          <th>6</th>
          <td>794538.317812</td>
          <td>2775504.193632</td>
          <td>2765302.000982</td>
          <td>2586476.416275</td>
          <td>2709538.756509</td>
          <td>2450307.128284</td>
          <td>1595568.711162</td>
          <td>818892.701581</td>
          <td>439955.979351</td>
        </tr>
      </tbody>
    </table>
    </div>



Step 4: Compare model predictions with measured data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Comparing the state level predictions with the actual data, we can see
where our model most under or overpredicts population for each
region/cohort combination.

.. code:: python

    diff = state_predictions-states['2010']
    diff.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>dec_1</th>
          <th>dec_2</th>
          <th>dec_3</th>
          <th>dec_4</th>
          <th>dec_5</th>
          <th>dec_6</th>
          <th>dec_7</th>
          <th>dec_8</th>
          <th>dec_9</th>
        </tr>
        <tr>
          <th>state</th>
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
          <th>1</th>
          <td>-219487.628119</td>
          <td>2599.213342</td>
          <td>15835.875334</td>
          <td>6809.201330</td>
          <td>4023.277920</td>
          <td>-1912.535100</td>
          <td>-5868.850592</td>
          <td>-2901.523388</td>
          <td>9196.525962</td>
        </tr>
        <tr>
          <th>2</th>
          <td>-37946.974341</td>
          <td>3419.612356</td>
          <td>-5552.269375</td>
          <td>-393.517636</td>
          <td>1535.883377</td>
          <td>-3307.106501</td>
          <td>1893.129879</td>
          <td>3905.875847</td>
          <td>1982.949764</td>
        </tr>
        <tr>
          <th>4</th>
          <td>-346203.194215</td>
          <td>-54529.978027</td>
          <td>-42145.290708</td>
          <td>-44857.927631</td>
          <td>-31554.166539</td>
          <td>-26378.167738</td>
          <td>-54246.591289</td>
          <td>-40817.456442</td>
          <td>-9747.847078</td>
        </tr>
        <tr>
          <th>5</th>
          <td>-145687.334069</td>
          <td>2479.388634</td>
          <td>7461.938099</td>
          <td>-756.696105</td>
          <td>279.524445</td>
          <td>-308.111210</td>
          <td>-8149.443344</td>
          <td>-5928.222301</td>
          <td>3645.643627</td>
        </tr>
        <tr>
          <th>6</th>
          <td>-1779080.682188</td>
          <td>-5492.806368</td>
          <td>-84180.999018</td>
          <td>-9240.583725</td>
          <td>54231.756509</td>
          <td>113788.128284</td>
          <td>106173.711162</td>
          <td>38316.701581</td>
          <td>-16261.020649</td>
        </tr>
      </tbody>
    </table>
    </div>



This is a little easier to understand if we weight it by the actual
measured population:

.. code:: python

    diff_percent = (state_predictions-states['2010'])/states['2010']
    diff_percent.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>dec_1</th>
          <th>dec_2</th>
          <th>dec_3</th>
          <th>dec_4</th>
          <th>dec_5</th>
          <th>dec_6</th>
          <th>dec_7</th>
          <th>dec_8</th>
          <th>dec_9</th>
        </tr>
        <tr>
          <th>state</th>
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
          <th>1</th>
          <td>-0.702124</td>
          <td>0.007677</td>
          <td>0.049297</td>
          <td>0.022888</td>
          <td>0.012502</td>
          <td>-0.006007</td>
          <td>-0.025573</td>
          <td>-0.023386</td>
          <td>0.162647</td>
        </tr>
        <tr>
          <th>2</th>
          <td>-0.715522</td>
          <td>0.065412</td>
          <td>-0.095456</td>
          <td>-0.008241</td>
          <td>0.029618</td>
          <td>-0.061051</td>
          <td>0.063381</td>
          <td>0.375854</td>
          <td>0.477704</td>
        </tr>
        <tr>
          <th>4</th>
          <td>-0.746436</td>
          <td>-0.116948</td>
          <td>-0.092592</td>
          <td>-0.106186</td>
          <td>-0.075417</td>
          <td>-0.069220</td>
          <td>-0.180489</td>
          <td>-0.228223</td>
          <td>-0.109223</td>
        </tr>
        <tr>
          <th>5</th>
          <td>-0.721864</td>
          <td>0.012090</td>
          <td>0.037886</td>
          <td>-0.004118</td>
          <td>0.001451</td>
          <td>-0.001638</td>
          <td>-0.056876</td>
          <td>-0.073063</td>
          <td>0.093658</td>
        </tr>
        <tr>
          <th>6</th>
          <td>-0.691276</td>
          <td>-0.001975</td>
          <td>-0.029543</td>
          <td>-0.003560</td>
          <td>0.020424</td>
          <td>0.048700</td>
          <td>0.071286</td>
          <td>0.049088</td>
          <td>-0.035643</td>
        </tr>
      </tbody>
    </table>
    </div>



Step 5: Merge with geo data to plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

I'm using geopandas to manage the shapefiles, and it has its own
plotting functionality. Unfortunately, it is not a particularly well
defined functionality.

.. code:: python

    geo_diff = state_geo.join(diff_percent)
    geo_diff.plot(column='dec_4')
    geo_diff.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>CensusDiv</th>
          <th>CensusReg</th>
          <th>FIPS</th>
          <th>FIPSNum</th>
          <th>Notes</th>
          <th>OBJECTID</th>
          <th>StateFIPS</th>
          <th>StateName</th>
          <th>XCentroid</th>
          <th>YCentroid</th>
          <th>geometry</th>
          <th>dec_1</th>
          <th>dec_2</th>
          <th>dec_3</th>
          <th>dec_4</th>
          <th>dec_5</th>
          <th>dec_6</th>
          <th>dec_7</th>
          <th>dec_8</th>
          <th>dec_9</th>
        </tr>
        <tr>
          <th>StateFIPSN</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
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
          <th>2</th>
          <td>Pacific</td>
          <td>West</td>
          <td>02000</td>
          <td>2000</td>
          <td>None</td>
          <td>1</td>
          <td>02</td>
          <td>Alaska</td>
          <td>-1882092.151950</td>
          <td>2310348.392810</td>
          <td>(POLYGON ((-2247528.774479387 2237995.01157197...</td>
          <td>-0.715522</td>
          <td>0.065412</td>
          <td>-0.095456</td>
          <td>-0.008241</td>
          <td>0.029618</td>
          <td>-0.061051</td>
          <td>0.063381</td>
          <td>0.375854</td>
          <td>0.477704</td>
        </tr>
        <tr>
          <th>53</th>
          <td>Pacific</td>
          <td>West</td>
          <td>53000</td>
          <td>53000</td>
          <td>None</td>
          <td>9</td>
          <td>53</td>
          <td>Washington</td>
          <td>-1837353.153170</td>
          <td>1340481.223852</td>
          <td>(POLYGON ((-2124362.24278068 1480441.850674443...</td>
          <td>-0.718560</td>
          <td>-0.006548</td>
          <td>-0.058893</td>
          <td>-0.069401</td>
          <td>-0.018494</td>
          <td>-0.031807</td>
          <td>-0.047478</td>
          <td>0.013500</td>
          <td>-0.030573</td>
        </tr>
        <tr>
          <th>23</th>
          <td>New England</td>
          <td>Northeast</td>
          <td>23000</td>
          <td>23000</td>
          <td>None</td>
          <td>10</td>
          <td>23</td>
          <td>Maine</td>
          <td>2068849.532637</td>
          <td>1172786.748295</td>
          <td>(POLYGON ((1951177.135094963 1127914.539498126...</td>
          <td>-0.682708</td>
          <td>0.073037</td>
          <td>0.147467</td>
          <td>0.085983</td>
          <td>-0.023217</td>
          <td>-0.055249</td>
          <td>-0.076098</td>
          <td>-0.034226</td>
          <td>-0.009394</td>
        </tr>
        <tr>
          <th>27</th>
          <td>West North Central</td>
          <td>Midwest</td>
          <td>27000</td>
          <td>27000</td>
          <td>None</td>
          <td>11</td>
          <td>27</td>
          <td>Minnesota</td>
          <td>131047.575089</td>
          <td>982130.006959</td>
          <td>POLYGON ((-91052.16805501282 1282100.079225723...</td>
          <td>-0.711546</td>
          <td>0.062669</td>
          <td>0.034611</td>
          <td>0.032717</td>
          <td>0.020127</td>
          <td>-0.019902</td>
          <td>0.043175</td>
          <td>0.022524</td>
          <td>-0.060437</td>
        </tr>
        <tr>
          <th>26</th>
          <td>East North Central</td>
          <td>Midwest</td>
          <td>26000</td>
          <td>26000</td>
          <td>None</td>
          <td>18</td>
          <td>26</td>
          <td>Michigan</td>
          <td>842567.889298</td>
          <td>809437.260865</td>
          <td>(POLYGON ((764918.7306621727 786184.882347865,...</td>
          <td>-0.657411</td>
          <td>0.082088</td>
          <td>0.197840</td>
          <td>0.176409</td>
          <td>0.088111</td>
          <td>0.032552</td>
          <td>0.050903</td>
          <td>0.075986</td>
          <td>0.011505</td>
        </tr>
      </tbody>
    </table>
    </div>




.. image:: Exploring_models_across_geographic_scales_files/Exploring_models_across_geographic_scales_33_1.png


Recipe Part B: fit state-by-state models
----------------------------------------

Now lets try optimizing the model's parameters specifically to each
state, and comparing with the national picture.

Step 1: Write the optimization functions to account for the state
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We'll start as before with functions that run the model and compute the
error (this time with a parameter for the information about the state in
question) and add a function to optimize and return the best fit
parameters for each state.

.. code:: python

    def exec_model(paramlist, state):
        params = dict(zip(['dec_%i_loss_rate'%i for i in range(1,10)], paramlist)) 
        output = model.run(initial_condition=(2000,state['2000']),
                           params=params, return_timestamps=2010).loc[2010]
        return output
    
    def error(paramlist, state):
        output = exec_model(paramlist, state)
        errors = output - state['2010']
        #don't tally errors in the first cohort, as we don't have info about births
        sse = sum(errors.values[1:]**2)
        return sse

Step 2: Apply optimization to each state
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We can wrap the optimizer in a function that takes census information
about each state and returns an optimized set of parameters for that
state. If we apply it to the states dataframe, we can get out a similar
dataframe that includes optimized parameters.

.. code:: python

    %%capture 
    def optimize_params(row):
        res = scipy.optimize.minimize(lambda x: error(x, row),
                                      x0=[.05]*9,
                                      method='L-BFGS-B');
        return pd.Series(index=['dec_%i_loss_rate'%i for i in range(1,10)], data=res['x'])
        
    state_fit_params = states.apply(optimize_params, axis=1)
    state_fit_params.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>dec_1_loss_rate</th>
          <th>dec_2_loss_rate</th>
          <th>dec_3_loss_rate</th>
          <th>dec_4_loss_rate</th>
          <th>dec_5_loss_rate</th>
          <th>dec_6_loss_rate</th>
          <th>dec_7_loss_rate</th>
          <th>dec_8_loss_rate</th>
          <th>dec_9_loss_rate</th>
        </tr>
        <tr>
          <th>state</th>
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
          <th>1</th>
          <td>0.021448</td>
          <td>-0.051229</td>
          <td>0.005996</td>
          <td>0.009159</td>
          <td>-0.006314</td>
          <td>-0.012721</td>
          <td>0.013077</td>
          <td>0.061467</td>
          <td>0.199157</td>
        </tr>
        <tr>
          <th>2</th>
          <td>0.024790</td>
          <td>-0.045179</td>
          <td>-0.021897</td>
          <td>0.015292</td>
          <td>-0.003120</td>
          <td>-0.023723</td>
          <td>0.039461</td>
          <td>0.137920</td>
          <td>0.200484</td>
        </tr>
        <tr>
          <th>4</th>
          <td>0.015650</td>
          <td>-0.066072</td>
          <td>-0.009319</td>
          <td>-0.003544</td>
          <td>-0.012930</td>
          <td>-0.018060</td>
          <td>-0.013545</td>
          <td>0.033047</td>
          <td>0.168508</td>
        </tr>
        <tr>
          <th>5</th>
          <td>0.022108</td>
          <td>-0.050841</td>
          <td>0.003923</td>
          <td>0.005605</td>
          <td>-0.006411</td>
          <td>-0.011430</td>
          <td>0.006571</td>
          <td>0.054650</td>
          <td>0.191023</td>
        </tr>
        <tr>
          <th>6</th>
          <td>0.020025</td>
          <td>-0.052080</td>
          <td>-0.006135</td>
          <td>0.010332</td>
          <td>-0.004042</td>
          <td>-0.004572</td>
          <td>0.025891</td>
          <td>0.065019</td>
          <td>0.148008</td>
        </tr>
      </tbody>
    </table>
    </div>



Step 3: Merge with geographic data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As we're looking at model parameters which themselves are multiplied by
populations to generate actual flows of people, we can look at the
difference between parameters directly without needing to normalize.

.. code:: python

    geo_diff = state_geo.join(state_fit_params)
    geo_diff.plot(column='dec_4_loss_rate')
    geo_diff.head(3)




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>CensusDiv</th>
          <th>CensusReg</th>
          <th>FIPS</th>
          <th>FIPSNum</th>
          <th>Notes</th>
          <th>OBJECTID</th>
          <th>StateFIPS</th>
          <th>StateName</th>
          <th>XCentroid</th>
          <th>YCentroid</th>
          <th>geometry</th>
          <th>dec_1_loss_rate</th>
          <th>dec_2_loss_rate</th>
          <th>dec_3_loss_rate</th>
          <th>dec_4_loss_rate</th>
          <th>dec_5_loss_rate</th>
          <th>dec_6_loss_rate</th>
          <th>dec_7_loss_rate</th>
          <th>dec_8_loss_rate</th>
          <th>dec_9_loss_rate</th>
        </tr>
        <tr>
          <th>StateFIPSN</th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
          <th></th>
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
          <th>2</th>
          <td>Pacific</td>
          <td>West</td>
          <td>02000</td>
          <td>2000</td>
          <td>None</td>
          <td>1</td>
          <td>02</td>
          <td>Alaska</td>
          <td>-1882092.151950</td>
          <td>2310348.392810</td>
          <td>(POLYGON ((-2247528.774479387 2237995.01157197...</td>
          <td>0.024790</td>
          <td>-0.045179</td>
          <td>-0.021897</td>
          <td>0.015292</td>
          <td>-0.003120</td>
          <td>-0.023723</td>
          <td>0.039461</td>
          <td>0.137920</td>
          <td>0.200484</td>
        </tr>
        <tr>
          <th>53</th>
          <td>Pacific</td>
          <td>West</td>
          <td>53000</td>
          <td>53000</td>
          <td>None</td>
          <td>9</td>
          <td>53</td>
          <td>Washington</td>
          <td>-1837353.153170</td>
          <td>1340481.223852</td>
          <td>(POLYGON ((-2124362.24278068 1480441.850674443...</td>
          <td>0.021844</td>
          <td>-0.053040</td>
          <td>-0.010785</td>
          <td>0.001392</td>
          <td>-0.006107</td>
          <td>-0.015620</td>
          <td>0.010874</td>
          <td>0.072777</td>
          <td>0.150871</td>
        </tr>
        <tr>
          <th>23</th>
          <td>New England</td>
          <td>Northeast</td>
          <td>23000</td>
          <td>23000</td>
          <td>None</td>
          <td>10</td>
          <td>23</td>
          <td>Maine</td>
          <td>2068849.532637</td>
          <td>1172786.748295</td>
          <td>(POLYGON ((1951177.135094963 1127914.539498126...</td>
          <td>0.025517</td>
          <td>-0.044513</td>
          <td>0.016994</td>
          <td>0.013372</td>
          <td>-0.014052</td>
          <td>-0.017986</td>
          <td>0.007721</td>
          <td>0.065287</td>
          <td>0.161693</td>
        </tr>
      </tbody>
    </table>
    </div>




.. image:: Exploring_models_across_geographic_scales_files/Exploring_models_across_geographic_scales_39_1.png


