
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

Loading data from CSV files
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pandas gives us a comprehensive set of tools for loading data from `a
variety of
sources <http://pandas.pydata.org/pandas-docs/version/0.18.1/io.html>`__,
including CSV, Excel, SQL, JSON, and Stata, amongst others. In this
demonstration, we'll read a comma separated value file of global
emissions data from the year 1751 until 2011.

The ``.read_csv`` method gives us options for how we want to format the
data as we read it in. In reading in our data file, we want to skip the
second row (indexed as ``1``!) and use the column ``Time`` as the index
of our resulting ``DataFrame``.

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
          <th>1757</th>
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
          <th>1759</th>
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
          <th>1761</th>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>1762</th>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>1763</th>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>1764</th>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>1765</th>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>1766</th>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>1767</th>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>1768</th>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>1769</th>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>1770</th>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>1771</th>
          <td>4</td>
          <td>0</td>
          <td>0</td>
          <td>4</td>
          <td>0</td>
          <td>0</td>
          <td>NaN</td>
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
          <th>1773</th>
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
          <th>1775</th>
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
          <th>1777</th>
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
          <th>1779</th>
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
          <th>1982</th>
          <td>5111</td>
          <td>738</td>
          <td>2196</td>
          <td>1992</td>
          <td>121</td>
          <td>64</td>
          <td>1.11</td>
        </tr>
        <tr>
          <th>1983</th>
          <td>5093</td>
          <td>739</td>
          <td>2176</td>
          <td>1995</td>
          <td>125</td>
          <td>58</td>
          <td>1.09</td>
        </tr>
        <tr>
          <th>1984</th>
          <td>5278</td>
          <td>807</td>
          <td>2199</td>
          <td>2094</td>
          <td>128</td>
          <td>51</td>
          <td>1.11</td>
        </tr>
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
        <tr>
          <th>1988</th>
          <td>5963</td>
          <td>935</td>
          <td>2412</td>
          <td>2414</td>
          <td>152</td>
          <td>50</td>
          <td>1.16</td>
        </tr>
        <tr>
          <th>1989</th>
          <td>6094</td>
          <td>982</td>
          <td>2459</td>
          <td>2457</td>
          <td>156</td>
          <td>41</td>
          <td>1.17</td>
        </tr>
        <tr>
          <th>1990</th>
          <td>6121</td>
          <td>1024</td>
          <td>2491</td>
          <td>2409</td>
          <td>157</td>
          <td>40</td>
          <td>1.15</td>
        </tr>
        <tr>
          <th>1991</th>
          <td>6198</td>
          <td>1050</td>
          <td>2603</td>
          <td>2340</td>
          <td>161</td>
          <td>44</td>
          <td>1.15</td>
        </tr>
        <tr>
          <th>1992</th>
          <td>6136</td>
          <td>1084</td>
          <td>2500</td>
          <td>2350</td>
          <td>167</td>
          <td>34</td>
          <td>1.12</td>
        </tr>
        <tr>
          <th>1993</th>
          <td>6133</td>
          <td>1117</td>
          <td>2513</td>
          <td>2291</td>
          <td>176</td>
          <td>36</td>
          <td>1.10</td>
        </tr>
        <tr>
          <th>1994</th>
          <td>6241</td>
          <td>1133</td>
          <td>2535</td>
          <td>2349</td>
          <td>186</td>
          <td>38</td>
          <td>1.10</td>
        </tr>
        <tr>
          <th>1995</th>
          <td>6374</td>
          <td>1152</td>
          <td>2559</td>
          <td>2430</td>
          <td>197</td>
          <td>36</td>
          <td>1.11</td>
        </tr>
        <tr>
          <th>1996</th>
          <td>6524</td>
          <td>1200</td>
          <td>2626</td>
          <td>2458</td>
          <td>203</td>
          <td>37</td>
          <td>1.12</td>
        </tr>
        <tr>
          <th>1997</th>
          <td>6624</td>
          <td>1196</td>
          <td>2698</td>
          <td>2483</td>
          <td>209</td>
          <td>38</td>
          <td>1.12</td>
        </tr>
        <tr>
          <th>1998</th>
          <td>6610</td>
          <td>1225</td>
          <td>2762</td>
          <td>2379</td>
          <td>209</td>
          <td>35</td>
          <td>1.11</td>
        </tr>
        <tr>
          <th>1999</th>
          <td>6597</td>
          <td>1258</td>
          <td>2740</td>
          <td>2349</td>
          <td>217</td>
          <td>33</td>
          <td>1.09</td>
        </tr>
        <tr>
          <th>2000</th>
          <td>6763</td>
          <td>1285</td>
          <td>2843</td>
          <td>2363</td>
          <td>226</td>
          <td>45</td>
          <td>1.10</td>
        </tr>
        <tr>
          <th>2001</th>
          <td>6929</td>
          <td>1312</td>
          <td>2845</td>
          <td>2489</td>
          <td>237</td>
          <td>46</td>
          <td>1.12</td>
        </tr>
        <tr>
          <th>2002</th>
          <td>6992</td>
          <td>1345</td>
          <td>2831</td>
          <td>2516</td>
          <td>252</td>
          <td>48</td>
          <td>1.11</td>
        </tr>
        <tr>
          <th>2003</th>
          <td>7405</td>
          <td>1390</td>
          <td>2957</td>
          <td>2735</td>
          <td>276</td>
          <td>47</td>
          <td>1.16</td>
        </tr>
        <tr>
          <th>2004</th>
          <td>7784</td>
          <td>1435</td>
          <td>3050</td>
          <td>2948</td>
          <td>298</td>
          <td>53</td>
          <td>1.21</td>
        </tr>
        <tr>
          <th>2005</th>
          <td>8076</td>
          <td>1477</td>
          <td>3075</td>
          <td>3146</td>
          <td>320</td>
          <td>59</td>
          <td>1.24</td>
        </tr>
        <tr>
          <th>2006</th>
          <td>8363</td>
          <td>1529</td>
          <td>3099</td>
          <td>3319</td>
          <td>356</td>
          <td>61</td>
          <td>1.27</td>
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

This syntax lets us select the first n rows:

::

    emissions.iloc[:5]

or, if we wish, the last n, using a minus sign to indicate counting from
the end of the ``DataFrame``:

::

    emissions.iloc[-5:]

or rows in the middle:

::

    emissions.iloc[10:20]

.. code:: python

    emissions.iloc[-3:]




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




.. parsed-literal::

    Year
    1751       3
    1752       3
    1753       3
    1754       3
    1755       3
    1756       3
    1757       3
    1758       3
    1759       3
    1760       3
    1761       3
    1762       3
    1763       3
    1764       3
    1765       3
    1766       3
    1767       3
    1768       3
    1769       3
    1770       3
    1771       4
    1772       4
    1773       4
    1774       4
    1775       4
    1776       4
    1777       4
    1778       4
    1779       4
    1780       4
            ... 
    1982    5111
    1983    5093
    1984    5278
    1985    5438
    1986    5606
    1987    5750
    1988    5963
    1989    6094
    1990    6121
    1991    6198
    1992    6136
    1993    6133
    1994    6241
    1995    6374
    1996    6524
    1997    6624
    1998    6610
    1999    6597
    2000    6763
    2001    6929
    2002    6992
    2003    7405
    2004    7784
    2005    8076
    2006    8363
    2007    8532
    2008    8740
    2009    8700
    2010    9140
    2011    9449
    Name: Total Emissions, dtype: int64



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
          <th>1756</th>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>1757</th>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>1758</th>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>1759</th>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>1760</th>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>1761</th>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>1762</th>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>1763</th>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>1764</th>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>1765</th>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>1766</th>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>1767</th>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>1768</th>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>1769</th>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>1770</th>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>1771</th>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>1772</th>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>1773</th>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>1774</th>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>1775</th>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>1776</th>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>1777</th>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>1778</th>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>1779</th>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>1780</th>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>...</th>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th>1982</th>
          <td>738</td>
          <td>2196</td>
        </tr>
        <tr>
          <th>1983</th>
          <td>739</td>
          <td>2176</td>
        </tr>
        <tr>
          <th>1984</th>
          <td>807</td>
          <td>2199</td>
        </tr>
        <tr>
          <th>1985</th>
          <td>835</td>
          <td>2186</td>
        </tr>
        <tr>
          <th>1986</th>
          <td>830</td>
          <td>2293</td>
        </tr>
        <tr>
          <th>1987</th>
          <td>892</td>
          <td>2306</td>
        </tr>
        <tr>
          <th>1988</th>
          <td>935</td>
          <td>2412</td>
        </tr>
        <tr>
          <th>1989</th>
          <td>982</td>
          <td>2459</td>
        </tr>
        <tr>
          <th>1990</th>
          <td>1024</td>
          <td>2491</td>
        </tr>
        <tr>
          <th>1991</th>
          <td>1050</td>
          <td>2603</td>
        </tr>
        <tr>
          <th>1992</th>
          <td>1084</td>
          <td>2500</td>
        </tr>
        <tr>
          <th>1993</th>
          <td>1117</td>
          <td>2513</td>
        </tr>
        <tr>
          <th>1994</th>
          <td>1133</td>
          <td>2535</td>
        </tr>
        <tr>
          <th>1995</th>
          <td>1152</td>
          <td>2559</td>
        </tr>
        <tr>
          <th>1996</th>
          <td>1200</td>
          <td>2626</td>
        </tr>
        <tr>
          <th>1997</th>
          <td>1196</td>
          <td>2698</td>
        </tr>
        <tr>
          <th>1998</th>
          <td>1225</td>
          <td>2762</td>
        </tr>
        <tr>
          <th>1999</th>
          <td>1258</td>
          <td>2740</td>
        </tr>
        <tr>
          <th>2000</th>
          <td>1285</td>
          <td>2843</td>
        </tr>
        <tr>
          <th>2001</th>
          <td>1312</td>
          <td>2845</td>
        </tr>
        <tr>
          <th>2002</th>
          <td>1345</td>
          <td>2831</td>
        </tr>
        <tr>
          <th>2003</th>
          <td>1390</td>
          <td>2957</td>
        </tr>
        <tr>
          <th>2004</th>
          <td>1435</td>
          <td>3050</td>
        </tr>
        <tr>
          <th>2005</th>
          <td>1477</td>
          <td>3075</td>
        </tr>
        <tr>
          <th>2006</th>
          <td>1529</td>
          <td>3099</td>
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



Arithmetic
~~~~~~~~~~

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
    1756       0
    1757       0
    1758       0
    1759       0
    1760       0
    1761       0
    1762       0
    1763       0
    1764       0
    1765       0
    1766       0
    1767       0
    1768       0
    1769       0
    1770       0
    1771       0
    1772       0
    1773       0
    1774       0
    1775       0
    1776       0
    1777       0
    1778       0
    1779       0
    1780       0
            ... 
    1982    2934
    1983    2915
    1984    3006
    1985    3021
    1986    3123
    1987    3198
    1988    3347
    1989    3441
    1990    3515
    1991    3653
    1992    3584
    1993    3630
    1994    3668
    1995    3711
    1996    3826
    1997    3894
    1998    3987
    1999    3998
    2000    4128
    2001    4157
    2002    4176
    2003    4347
    2004    4485
    2005    4552
    2006    4628
    2007    4643
    2008    4732
    2009    4621
    2010    4798
    2011    4897
    dtype: int64



Simple operations
~~~~~~~~~~~~~~~~~

A number of simple operations are built into Pandas to facilitate
working with the data. For example, we can show `descriptive
statistics <http://pandas.pydata.org/pandas-docs/version/0.18.1/basics.html#descriptive-statistics>`__
such as the maximum value of each column:

.. code:: python

    emissions.max()




.. parsed-literal::

    Total Emissions         9449.00
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




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Predator Population</th>
          <th>Prey Population</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0.000000</th>
          <td>100.000000</td>
          <td>2.500000e+02</td>
        </tr>
        <tr>
          <th>0.015625</th>
          <td>100.375000</td>
          <td>2.577734e+02</td>
        </tr>
        <tr>
          <th>0.031250</th>
          <td>100.763598</td>
          <td>2.657884e+02</td>
        </tr>
        <tr>
          <th>0.046875</th>
          <td>101.166319</td>
          <td>2.740525e+02</td>
        </tr>
        <tr>
          <th>0.062500</th>
          <td>101.583713</td>
          <td>2.825733e+02</td>
        </tr>
        <tr>
          <th>0.078125</th>
          <td>102.016354</td>
          <td>2.913589e+02</td>
        </tr>
        <tr>
          <th>0.093750</th>
          <td>102.464841</td>
          <td>3.004174e+02</td>
        </tr>
        <tr>
          <th>0.109375</th>
          <td>102.929803</td>
          <td>3.097573e+02</td>
        </tr>
        <tr>
          <th>0.125000</th>
          <td>103.411897</td>
          <td>3.193874e+02</td>
        </tr>
        <tr>
          <th>0.140625</th>
          <td>103.911808</td>
          <td>3.293167e+02</td>
        </tr>
        <tr>
          <th>0.156250</th>
          <td>104.430258</td>
          <td>3.395543e+02</td>
        </tr>
        <tr>
          <th>0.171875</th>
          <td>104.967999</td>
          <td>3.501100e+02</td>
        </tr>
        <tr>
          <th>0.187500</th>
          <td>105.525822</td>
          <td>3.609935e+02</td>
        </tr>
        <tr>
          <th>0.203125</th>
          <td>106.104555</td>
          <td>3.722151e+02</td>
        </tr>
        <tr>
          <th>0.218750</th>
          <td>106.705065</td>
          <td>3.837851e+02</td>
        </tr>
        <tr>
          <th>0.234375</th>
          <td>107.328264</td>
          <td>3.957144e+02</td>
        </tr>
        <tr>
          <th>0.250000</th>
          <td>107.975109</td>
          <td>4.080141e+02</td>
        </tr>
        <tr>
          <th>0.265625</th>
          <td>108.646603</td>
          <td>4.206957e+02</td>
        </tr>
        <tr>
          <th>0.281250</th>
          <td>109.343801</td>
          <td>4.337710e+02</td>
        </tr>
        <tr>
          <th>0.296875</th>
          <td>110.067813</td>
          <td>4.472522e+02</td>
        </tr>
        <tr>
          <th>0.312500</th>
          <td>110.819803</td>
          <td>4.611520e+02</td>
        </tr>
        <tr>
          <th>0.328125</th>
          <td>111.601000</td>
          <td>4.754831e+02</td>
        </tr>
        <tr>
          <th>0.343750</th>
          <td>112.412693</td>
          <td>4.902590e+02</td>
        </tr>
        <tr>
          <th>0.359375</th>
          <td>113.256243</td>
          <td>5.054935e+02</td>
        </tr>
        <tr>
          <th>0.375000</th>
          <td>114.133083</td>
          <td>5.212007e+02</td>
        </tr>
        <tr>
          <th>0.390625</th>
          <td>115.044722</td>
          <td>5.373953e+02</td>
        </tr>
        <tr>
          <th>0.406250</th>
          <td>115.992754</td>
          <td>5.540923e+02</td>
        </tr>
        <tr>
          <th>0.421875</th>
          <td>116.978860</td>
          <td>5.713073e+02</td>
        </tr>
        <tr>
          <th>0.437500</th>
          <td>118.004814</td>
          <td>5.890562e+02</td>
        </tr>
        <tr>
          <th>0.453125</th>
          <td>119.072493</td>
          <td>6.073556e+02</td>
        </tr>
        <tr>
          <th>...</th>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th>49.546875</th>
          <td>97519.038826</td>
          <td>1.006829e-232</td>
        </tr>
        <tr>
          <th>49.562500</th>
          <td>97503.801477</td>
          <td>8.848783e-233</td>
        </tr>
        <tr>
          <th>49.578125</th>
          <td>97488.566508</td>
          <td>7.777199e-233</td>
        </tr>
        <tr>
          <th>49.593750</th>
          <td>97473.333919</td>
          <td>6.835567e-233</td>
        </tr>
        <tr>
          <th>49.609375</th>
          <td>97458.103711</td>
          <td>6.008108e-233</td>
        </tr>
        <tr>
          <th>49.625000</th>
          <td>97442.875882</td>
          <td>5.280957e-233</td>
        </tr>
        <tr>
          <th>49.640625</th>
          <td>97427.650433</td>
          <td>4.641937e-233</td>
        </tr>
        <tr>
          <th>49.656250</th>
          <td>97412.427362</td>
          <td>4.080352e-233</td>
        </tr>
        <tr>
          <th>49.671875</th>
          <td>97397.206670</td>
          <td>3.586806e-233</td>
        </tr>
        <tr>
          <th>49.687500</th>
          <td>97381.988357</td>
          <td>3.153042e-233</td>
        </tr>
        <tr>
          <th>49.703125</th>
          <td>97366.772421</td>
          <td>2.771810e-233</td>
        </tr>
        <tr>
          <th>49.718750</th>
          <td>97351.558863</td>
          <td>2.436738e-233</td>
        </tr>
        <tr>
          <th>49.734375</th>
          <td>97336.347682</td>
          <td>2.142229e-233</td>
        </tr>
        <tr>
          <th>49.750000</th>
          <td>97321.138878</td>
          <td>1.883366e-233</td>
        </tr>
        <tr>
          <th>49.765625</th>
          <td>97305.932450</td>
          <td>1.655829e-233</td>
        </tr>
        <tr>
          <th>49.781250</th>
          <td>97290.728398</td>
          <td>1.455820e-233</td>
        </tr>
        <tr>
          <th>49.796875</th>
          <td>97275.526721</td>
          <td>1.280006e-233</td>
        </tr>
        <tr>
          <th>49.812500</th>
          <td>97260.327420</td>
          <td>1.125454e-233</td>
        </tr>
        <tr>
          <th>49.828125</th>
          <td>97245.130494</td>
          <td>9.895900e-234</td>
        </tr>
        <tr>
          <th>49.843750</th>
          <td>97229.935943</td>
          <td>8.701509e-234</td>
        </tr>
        <tr>
          <th>49.859375</th>
          <td>97214.743765</td>
          <td>7.651483e-234</td>
        </tr>
        <tr>
          <th>49.875000</th>
          <td>97199.553961</td>
          <td>6.728346e-234</td>
        </tr>
        <tr>
          <th>49.890625</th>
          <td>97184.366531</td>
          <td>5.916744e-234</td>
        </tr>
        <tr>
          <th>49.906250</th>
          <td>97169.181474</td>
          <td>5.203182e-234</td>
        </tr>
        <tr>
          <th>49.921875</th>
          <td>97153.998789</td>
          <td>4.575798e-234</td>
        </tr>
        <tr>
          <th>49.937500</th>
          <td>97138.818477</td>
          <td>4.024172e-234</td>
        </tr>
        <tr>
          <th>49.953125</th>
          <td>97123.640536</td>
          <td>3.539141e-234</td>
        </tr>
        <tr>
          <th>49.968750</th>
          <td>97108.464968</td>
          <td>3.112654e-234</td>
        </tr>
        <tr>
          <th>49.984375</th>
          <td>97093.291770</td>
          <td>2.737635e-234</td>
        </tr>
        <tr>
          <th>50.000000</th>
          <td>97078.120943</td>
          <td>2.407864e-234</td>
        </tr>
      </tbody>
    </table>
    <p>3201 rows × 2 columns</p>
    </div>



In this case, may want to downsample the returned data to make it more
manageable:

.. code:: python

    sim_result_df.loc[range(50)]




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Predator Population</th>
          <th>Prey Population</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>100.000000</td>
          <td>2.500000e+02</td>
        </tr>
        <tr>
          <th>1</th>
          <td>211.552891</td>
          <td>1.768835e+03</td>
        </tr>
        <tr>
          <th>2</th>
          <td>26037.148846</td>
          <td>9.285526e+03</td>
        </tr>
        <tr>
          <th>3</th>
          <td>155329.734184</td>
          <td>3.478882e-02</td>
        </tr>
        <tr>
          <th>4</th>
          <td>153784.453003</td>
          <td>9.557026e-09</td>
        </tr>
        <tr>
          <th>5</th>
          <td>152254.153168</td>
          <td>3.189036e-15</td>
        </tr>
        <tr>
          <th>6</th>
          <td>150739.081255</td>
          <td>1.289315e-21</td>
        </tr>
        <tr>
          <th>7</th>
          <td>149239.085730</td>
          <td>6.300084e-28</td>
        </tr>
        <tr>
          <th>8</th>
          <td>147754.016571</td>
          <td>3.711618e-34</td>
        </tr>
        <tr>
          <th>9</th>
          <td>146283.725246</td>
          <td>2.630076e-40</td>
        </tr>
        <tr>
          <th>10</th>
          <td>144828.064701</td>
          <td>2.236332e-46</td>
        </tr>
        <tr>
          <th>11</th>
          <td>143386.889347</td>
          <td>2.276449e-52</td>
        </tr>
        <tr>
          <th>12</th>
          <td>141960.055042</td>
          <td>2.767832e-58</td>
        </tr>
        <tr>
          <th>13</th>
          <td>140547.419079</td>
          <td>4.010544e-64</td>
        </tr>
        <tr>
          <th>14</th>
          <td>139148.840172</td>
          <td>6.910118e-70</td>
        </tr>
        <tr>
          <th>15</th>
          <td>137764.178439</td>
          <td>1.412661e-75</td>
        </tr>
        <tr>
          <th>16</th>
          <td>136393.295392</td>
          <td>3.419214e-81</td>
        </tr>
        <tr>
          <th>17</th>
          <td>135036.053919</td>
          <td>9.777569e-87</td>
        </tr>
        <tr>
          <th>18</th>
          <td>133692.318275</td>
          <td>3.296444e-92</td>
        </tr>
        <tr>
          <th>19</th>
          <td>132361.954063</td>
          <td>1.307611e-97</td>
        </tr>
        <tr>
          <th>20</th>
          <td>131044.828225</td>
          <td>6.090458e-103</td>
        </tr>
        <tr>
          <th>21</th>
          <td>129740.809027</td>
          <td>3.324255e-108</td>
        </tr>
        <tr>
          <th>22</th>
          <td>128449.766046</td>
          <td>2.122064e-113</td>
        </tr>
        <tr>
          <th>23</th>
          <td>127171.570156</td>
          <td>1.581256e-118</td>
        </tr>
        <tr>
          <th>24</th>
          <td>125906.093516</td>
          <td>1.372768e-123</td>
        </tr>
        <tr>
          <th>25</th>
          <td>124653.209558</td>
          <td>1.385885e-128</td>
        </tr>
        <tr>
          <th>26</th>
          <td>123412.792973</td>
          <td>1.624011e-133</td>
        </tr>
        <tr>
          <th>27</th>
          <td>122184.719699</td>
          <td>2.204904e-138</td>
        </tr>
        <tr>
          <th>28</th>
          <td>120968.866908</td>
          <td>3.462173e-143</td>
        </tr>
        <tr>
          <th>29</th>
          <td>119765.112994</td>
          <td>6.276195e-148</td>
        </tr>
        <tr>
          <th>30</th>
          <td>118573.337564</td>
          <td>1.311216e-152</td>
        </tr>
        <tr>
          <th>31</th>
          <td>117393.421419</td>
          <td>3.151627e-157</td>
        </tr>
        <tr>
          <th>32</th>
          <td>116225.246549</td>
          <td>8.700438e-162</td>
        </tr>
        <tr>
          <th>33</th>
          <td>115068.696116</td>
          <td>2.754017e-166</td>
        </tr>
        <tr>
          <th>34</th>
          <td>113923.654447</td>
          <td>9.979186e-171</td>
        </tr>
        <tr>
          <th>35</th>
          <td>112790.007019</td>
          <td>4.132575e-175</td>
        </tr>
        <tr>
          <th>36</th>
          <td>111667.640449</td>
          <td>1.952753e-179</td>
        </tr>
        <tr>
          <th>37</th>
          <td>110556.442480</td>
          <td>1.051208e-183</td>
        </tr>
        <tr>
          <th>38</th>
          <td>109456.301976</td>
          <td>6.436765e-188</td>
        </tr>
        <tr>
          <th>39</th>
          <td>108367.108903</td>
          <td>4.476281e-192</td>
        </tr>
        <tr>
          <th>40</th>
          <td>107288.754325</td>
          <td>3.530039e-196</td>
        </tr>
        <tr>
          <th>41</th>
          <td>106221.130389</td>
          <td>3.152138e-200</td>
        </tr>
        <tr>
          <th>42</th>
          <td>105164.130314</td>
          <td>3.182398e-204</td>
        </tr>
        <tr>
          <th>43</th>
          <td>104117.648383</td>
          <td>3.627406e-208</td>
        </tr>
        <tr>
          <th>44</th>
          <td>103081.579931</td>
          <td>4.661307e-212</td>
        </tr>
        <tr>
          <th>45</th>
          <td>102055.821334</td>
          <td>6.743337e-216</td>
        </tr>
        <tr>
          <th>46</th>
          <td>101040.269999</td>
          <td>1.096711e-219</td>
        </tr>
        <tr>
          <th>47</th>
          <td>100034.824354</td>
          <td>2.002451e-223</td>
        </tr>
        <tr>
          <th>48</th>
          <td>99039.383839</td>
          <td>4.099159e-227</td>
        </tr>
        <tr>
          <th>49</th>
          <td>98053.848891</td>
          <td>9.395273e-231</td>
        </tr>
      </tbody>
    </table>
    </div>



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
